#!/bin/bash

ls /var/opt/mssql/backup

# adding OLTP database
/opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -P dscPass24! -C -Q 'restore filelistonly from disk="/var/opt/mssql/backup/AdventureWorks2019.bak"'
/opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -P dscPass24! -C -Q 'RESTORE DATABASE AdventureWorks2019 FROM DISK="/var/opt/mssql/backup/AdventureWorks2019.bak" WITH
MOVE "AdventureWorks2019" to "/var/opt/mssql/data/AdventureWorks2019.mdf",
MOVE "AdventureWorks2019_log" to "/var/opt/mssql/data/AdventureWorks2019_log.ldf"'

# adding OLAP database
/opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -P dscPass24! -C -Q 'restore filelistonly from disk="/var/opt/mssql/backup/AdventureWorksDW2019.bak"'
/opt/mssql-tools18/bin/sqlcmd -S 127.0.0.1 -U sa -P dscPass24! -C -Q 'RESTORE DATABASE AdventureWorksDW2019 FROM DISK="/var/opt/mssql/backup/AdventureWorksDW2019.bak" WITH
MOVE "AdventureWorksDW2019" to "/var/opt/mssql/data/AdventureWorksDW2019.mdf",
MOVE "AdventureWorksDW2019_log" to "/var/opt/mssql/data/AdventureWorksDW2019_log.ldf"'