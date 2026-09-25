from setuptools import setup

setup(
    name='data_dashboard',
    version='0.1.0',
    description='PEACE data dashboard blueprint (pluggable Parquet/DuckDB or ElasticSearch backends)',
    packages=['data_dashboard', 'data_dashboard.backends'],
    include_package_data=True,
    package_data={
        'data_dashboard': ['settings.ini', 'atlas/*.csv', 'web/*', 'web/**/*'],
    },
    install_requires=[
        'Flask>=2.0.0',
        'Flask-Login',
        'duckdb>=0.9',
        'pandas',
        'numpy',
    ],
)
