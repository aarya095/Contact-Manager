"""drop_unique_constraint

Revision ID: 9618de31406f
Revises: 96293ddbdffd
Create Date: 2026-05-07 18:43:13.754227

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '9618de31406f'
down_revision: Union[str, Sequence[str], None] = '96293ddbdffd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    op.drop_constraint(
        constraint_name = 'uq_contacts_contact_name',
        table_name = "contacts",
        type_ = "unique"
        )
    op.drop_constraint(
        constraint_name = 'uq_contacts_contact_number',
        table_name = "contacts",
        type_ = "unique"
        )


def downgrade() -> None:
    """Downgrade schema."""
    op.create_unique_constraint(
        constraint_name = 'uq_contacts_contact_name',
        table_name = "contacts",
        columns = ["contact_name"]
    )
    op.create_unique_constraint(
        constraint_name = 'uq_contacts_contact_number',
        table_name = "contacts",
        columns = ["contact_number"]
    )