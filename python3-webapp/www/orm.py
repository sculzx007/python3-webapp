#!/usr/bin/env python3
# -*- coding: utf-8 -*-
__author__ = 'lzx'

import logging, aiomysql, asyncio

def log(sql, args=()):
    logging.info('SQL: %s' % sql)

#创建连接池，便于每个HTTP请求都可以从连接池中直接获取数据库连接
async def create_pool(loop, **kw):
    logging.info('Create database connection pool...')
    global __pool                              # 连接池由全局变量 __pool 存储，默认情况下，将编码设置为utf-8，自动提交事务
    __pool = await aiomysql.create_pool(host= kw.get('host', 'localhost'),
                                        port= kw.get('port', 3306),
                                        user= kw['user'],
                                        password= kw['password'],
                                        db= kw['db'],
                                        charset= kw.get('charset', 'utf8'),
                                        autocommit= kw.get('autocommit', True),
                                        maxsize= kw.get('maxsize', 10),
                                        minsize= kw.get('minsize', 1),
                                        loop= loop)

# Select语句
async def select(sql, args, size=None):
    log(sql, args)
    global __pool
    async with __pool.get() as conn:
        cur = await conn.cursor(aiomysql.DictCursor)
        await cur.execute(sql.replace('?', '%s'), args or ())       #SQL占位符是？，而MySQL占位符是%s，这行代码是使select()函数在内部自动替换
        if size:                             #如果传入了size参数，就通过fetchmany()获取最多指定数量的记录
            rs = await cur.fetchmany(size)          #在一个协程（cur）中调用另一个协程（rs）
        else:
            rs = await cur.fetchall()       #如果没有传入size参数，就通过fetchall()获取所有数量的记录
        await cur.close()
        logging.info('Rows returned: %s' % len(rs))
        return rs                          # 获得子协程（rs）的返回结果

# Insert，Update，Delete语句
# 由于Insert，Update，Delete语句的执行都需要相同的参数，返回一个整数表示影响的行数
async def execute(sql, args, autocommit=True):
    log(sql)
    global _pool
    async with _pool.get() as conn:
        if not autocommit:
            await conn.begin()
        try:
            cur = await conn.cursor
            await cur.execute(sql.replace('?', '%s'), args)
            affected = cur.rowcount
            await cur.close()
            if not autocommit:
                await conn.commit()
        except BaseException as e:
            if not autocommit:
                await conn.rollback()
            raise
        return affected

# Filed类及其子类
class Field(object):
    def __init__(self, name, column_type, primary_key, default):
        self.name = name
        self.column_type = column_type
        self.primary_key = primary_key
        self.default = default

    def __str__(self):
        return '<%s, %s: %s>' % (self.__class__.__name__, self.column_type, self.name)

#映射字符串的StringFeild
class StringFeild(Field):
    def __init__(self, name = None, primary_key = False, default = None,  ddl = 'varchar(100)'):
        super().__init__(name, ddl, primary_key, default)

# Bool型
class BooleanField(Field):
    def __init__(self, name = None, default = False):
        super().__init__(name, 'boolean', False, default)

# 整数型
class IntegerField(Field):
    def __init__(self, name = None, primary_key = Field, default = 0):
        super().__init__(name, 'bigint', primary_key, default)

# 浮点型
class FloatField(Field):
    def __init__(self, name = None, primary_key = False, default = 0.0):
        super().__init__(name, 'real', primary_key, default)

# 文本型
class TextField(Field):
    def __init__(self, name = None, default = None):
        super.__init__(name, 'text', False, default)

# Model的元类
class ModelMetaclass(type):
    def __new__(cls, name, bases, attrs):
        #首先排除Model类本身
        if name == 'Model':
            return type.__new__(cls, name, bases, attrs)

        #获取table名称
        tableName = attrs.get('__table__', None) or name
        logging.info('Found model: %s (table: %s)' % (name, tableName))

        #获取所有的Field和主键名
        mappings = dict()
        fields = []
        primaryKey = None
        for k, v, in attrs.items():
            if isinstance(v, Field):
                logging.info('Found mapping: %s ==> %s' % (k, v))
                mappings[k] = v
                if v.primary_key:
                    #找到主键
                    if primaryKey:
                        raise RuntimeError('Duplicate primary key for field: %s' % k)
                    primaryKey = k
                else:
                    fields.append(k)
        if not primaryKey:
            raise RuntimeError('Primary key not found')
        for k in mappings.keys():
            attrs.pop(k)

        escaped_fields = list(map(lambda f: '`%s`' % f, fields))
        attrs['__mapping__'] = mappings        #保存属性和列的映射关系
        attrs['__table__'] = tableName         #保存列名
        attrs['__primary_key__'] = primaryKey   #主键属性名
        attrs['__fields__'] = fields            #除主键外的属性名

        #构造默认的SELECT，INSERT，UPDATE和DELETE语句
        attrs['__select__'] = 'select %s, `%s` from `%s`' % (primaryKey, ', '.join(escaped_fields), tableName)
        attrs['__insert__'] = 'insert into `%s` (%s, `%s`) value (%s)' % (tableName, ', '.join(escaped_fields), primaryKey, create_args_string(len(escaped_fields) + 1))
        attrs['__update__'] = 'update `%s` set %s where `%s`=?' % (tableName, ', '.join(map(lambda f: '`s`=?' % (mappings.get(f).name or f), fields)), primaryKey)
        attrs['__delete__'] = 'delete from `%s` where `%s`=?' % (tableName, primaryKey)
        return type.__new__(cls, name, bases, attrs)

#定义所有ORM映射的基类Model
class Model(dict, metaclass= ModelMetaclass):   # Model从dict类继承
    def __init__(self, **kw):
        super(Model, self).__init__(**kw)

    def __getattr__(self, key):
        try:
            return self[key]
        except KeyError:
            raise AttributeError(r"Model's object has no attribute '%s'" % key)

    def __setattr__(self, key, value):
        self[key] = value

    def getValue(self, key):
        return getattr(self, key, None)

    def getValueOrDefault(self, key):
        value = getattr(self, key, None)
        if value is None:
            field = self.__mapping__[key]
            if field.default is not None:
                value = field.default() if callable(field.default) else field.default
                logging.debug('Using default value for %s: %s' % (key, str(value)))
                setattr(self, key, value)
        return value

    # 根据where条件查找
    @classmethod
    async def findAll(cls, where = None, args = None, **kw):
        'find objects by where clause'
        sql = [cls.__select__]
        if where:
            sql.append('where')
            sql.append(where)
        if args is None:
            args = []

        orderBy = kw.get('orderBy', None)
        if orderBy:
            sql.append('order by')
            sql.append(orderBy)

        limit = kw.get('limit', None)
        if limit is not None:
            sql.append('limit')
            if isinstance(limit, int):
                sql.append('?')
                args.append(limit)
            elif isinstance(limit, tuple) and len(limit) == 2:
                sql.append('?, ?')
                args.extend(limit)
            else:
                raise ValueError('Invalid limit value: %s' % str(limit))
        rs = await select(' '.join(sql), args)
        return [cls(**r) for r in rs]

    # 根据where条件查找，但返回的是整数，适用于select count(*) 类型的SQL
    @classmethod
    async def findNumber(cls, selectField, where = None, args = None):
        'find number by select and where'
        sql = ['select %s _num_ from `%s`' % (selectField, cls.__table__)]

        if where:
            sql.append('where')
            sql.append(where)

        rs = await select(' '.join(sql), args, 1)
        if len(rs) == 0:
            return None
        return rs[0]['_num_']

    # 主键查找
    @classmethod
    async def find(cls, primary_key):
        'find object by primary key'
        rs = await select('%s where `%s`=?' % (cls.__select__, cls.__primary_key__), [primary_key], 1)
        if len(rs) == 0:
            return None
        return cls(**rs[0])

    # 保存
    async def save(self):
        args = list(map(self.getValueOrDefault, self.__fields__))
        args.append(self.getValueOrDefault(self.__primary_key__))
        rows = await execute(self.__insert__, args)
        if rows != 1:
            logging.warn('failed to insert record: affected rows: %s' % rows)

    # 更新
    async def update(self):
        args = list(map(self.getValue, self.__fields__))
        args.append(self.getValue(self.__primary_key__))
        rows = await execute(self.__update__, args)
        if rows != 1:
            logging.warn('failed to update by primary key: affected rows: %s' % rows)

    # 移除
    async def remove(self):
        args = [self.getValue(self.__primary_key__)]
        rows = await execute(self.__delete__, args)
        if rows != 1:
            logging.warn('failed to remove by primary key: affected rows: %s' % rows)






