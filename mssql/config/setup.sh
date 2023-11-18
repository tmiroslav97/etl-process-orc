#!/bin/bash

ls /var/opt/mssql/backup
/opt/mssql-tools/bin/sqlcmd -S 127.0.0.1 -U sa -P dscPass23! -Q 'restore filelistonly from disk="/var/opt/mssql/backup/AdventureWorks2017.bak"'
/opt/mssql-tools/bin/sqlcmd -S 127.0.0.1 -U sa -P dscPass23! -Q 'RESTORE DATABASE AdventureWorks2017 FROM DISK="/var/opt/mssql/backup/AdventureWorks2017.bak" WITH
MOVE "AdventureWorks2017" to "/var/opt/mssql/data/AdventureWorks2017.mdf",
MOVE "AdventureWorks2017_log" to "/var/opt/mssql/data/AdventureWorks2017_log.ldf"'