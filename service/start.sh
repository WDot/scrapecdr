#!/bin/bash
public_mm/bin/install.sh << EOF
/app/public_mm
/usr/bin/java
EOF

public_mm/bin/wsdserverctl start
public_mm/bin/skrmedpostctl start

python3 main.py