from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
deputado = Table('deputado', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('nome', String(length=50)),
    Column('partido', String(length=10)),
    Column('email', String(length=50)),
    Column('profissao', String(length=60)),
    Column('telefone', String(length=20)),
    Column('biografia', String(length=300)),
)

projeto = Table('projeto', post_meta,
    Column('numero', String(length=20), primary_key=True, nullable=False),
    Column('nome', String(length=50)),
    Column('texto', String(length=200)),
    Column('status', String(length=10)),
    Column('dataPublicacao', DateTime),
    Column('deputado_id', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['deputado'].create()
    post_meta.tables['projeto'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['deputado'].drop()
    post_meta.tables['projeto'].drop()
