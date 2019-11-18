"""
Basic Configuration File
"""

version: str = 'Vanilla 0.0.1'
host: str = '0.0.0.0'
port: int = 5000

debug: bool = True

SQLALCHEMY_TRACK_MODIFICATIONS: bool = False
SQLALCHEMY_DATABASE_URI: str = 'mysql+pymysql://QuickReportApp:password@localhost:3306/qr_report_v1'
# TODO: PASSWORD FOR DATABASE SHOULD BE RELOCATED IN PRODUCTION
