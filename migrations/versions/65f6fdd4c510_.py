"""empty message

Revision ID: 65f6fdd4c510
Revises: 
Create Date: 2021-12-10 12:41:09.712670

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '65f6fdd4c510'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('patients',
    sa.Column('cpf', sa.String(length=11), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('age', sa.Integer(), nullable=True),
    sa.Column('gender', sa.String(length=20), nullable=True),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('health_insurance', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('cpf'),
    sa.UniqueConstraint('email')
    )
    op.create_table('professionals',
    sa.Column('council_number', sa.String(length=20), nullable=False),
    sa.Column('name', sa.String(length=50), nullable=False),
    sa.Column('email', sa.String(length=50), nullable=False),
    sa.Column('phone', sa.String(length=20), nullable=True),
    sa.Column('specialty', sa.String(length=20), nullable=False),
    sa.Column('address', sa.String(length=50), nullable=True),
    sa.Column('password_hash', sa.String(), nullable=True),
    sa.Column('active', sa.Boolean(), nullable=True),
    sa.PrimaryKeyConstraint('council_number'),
    sa.UniqueConstraint('email')
    )
    op.create_table('appointments',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.String(length=11), nullable=False),
    sa.Column('professionals_id', sa.String(length=20), nullable=False),
    sa.Column('date', sa.DateTime(), nullable=False),
    sa.Column('finished', sa.Boolean(), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.cpf'], ),
    sa.ForeignKeyConstraint(['professionals_id'], ['professionals.council_number'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('date')
    )
    op.create_table('professionals_patients',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('patient_id', sa.String(length=11), nullable=True),
    sa.Column('professionals_id', sa.String(length=20), nullable=True),
    sa.ForeignKeyConstraint(['patient_id'], ['patients.cpf'], ),
    sa.ForeignKeyConstraint(['professionals_id'], ['professionals.council_number'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('professionals_patients')
    op.drop_table('appointments')
    op.drop_table('professionals')
    op.drop_table('patients')
    # ### end Alembic commands ###
