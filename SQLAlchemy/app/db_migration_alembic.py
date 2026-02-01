"""
===========================================================
SQLAlchemy Database Migration with Alembic — Complete Guide
===========================================================

Definition:
Alembic is a lightweight database migration tool for SQLAlchemy.
It helps manage schema changes over time, ensuring version control
for your database structure.

Use Cases:
- Add/remove columns
- Create/drop tables
- Alter constraints
- Keep DB in sync with models

This file explains:
- Installing Alembic
- Initial setup
- Creating migration scripts
- Running migrations
- Upgrading/downgrading
- Best practices
"""

# =========================================================
# 1. Install Alembic
# =========================================================
"""
pip install alembic
"""

# =========================================================
# 2. Initialize Alembic in your project
# =========================================================
"""
alembic init alembic

This creates:
- alembic/ directory
  - env.py       -> migration environment
  - script.py.mako -> migration template
  - versions/   -> stores migration scripts
- alembic.ini   -> config file for DB URL and settings
"""

# =========================================================
# 3. Configure alembic.ini
# =========================================================
"""
Edit alembic.ini:

sqlalchemy.url = sqlite:///alembic_example.db
# or your DB URL
"""

# =========================================================
# 4. Link Models in env.py
# =========================================================
"""
Inside env.py, import your Base metadata:

from my_models import Base  # your declarative_base()
target_metadata = Base.metadata
"""

# =========================================================
# 5. Create Migration Script
# =========================================================
"""
Generate an automatic migration:

alembic revision --autogenerate -m "create users table"

- This creates a new file in versions/
- The file contains upgrade() and downgrade() functions
"""

# =========================================================
# 6. Example upgrade/downgrade
# =========================================================
"""
# Alembic auto-generated example

def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('email', sa.String(), nullable=True)
    )

def downgrade():
    op.drop_table('users')
"""

# =========================================================
# 7. Apply Migration
# =========================================================
"""
Upgrade database:

alembic upgrade head

- head refers to the latest revision
- Database schema is updated
"""

# =========================================================
# 8. Downgrade Migration
# =========================================================
"""
Rollback to previous version:

alembic downgrade -1
or
alembic downgrade <revision_id>
"""

# =========================================================
# 9. Tips & Best Practices
# =========================================================
"""
- Always keep your models and Alembic metadata in sync
- Use --autogenerate to reduce errors
- Review auto-generated scripts before applying
- Store migration scripts in Git for version control
- Use descriptive messages for revisions
- Use multiple branches carefully with Alembic

Commands Summary:
- alembic init <dir>        -> initialize Alembic
- alembic revision -m "msg" -> create migration
- alembic revision --autogenerate -m "msg" -> auto migration
- alembic upgrade head      -> apply latest migration
- alembic downgrade -1      -> rollback one migration
"""

# =========================================================
# Summary
# =========================================================
"""
Alembic integrates with SQLAlchemy ORM for smooth DB migrations.
It supports versioned, reversible schema changes, ideal for:
- Multi-developer projects
- Production databases
- Incremental schema evolution

Using Alembic ensures your database always matches your models,
with safe upgrades and rollbacks.
"""

"""
===========================================================
END OF FILE
===========================================================

Save as:
sqlalchemy_alembic_migration.txt

Push to GitHub as advanced ORM + migration concept.
"""
