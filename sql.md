## Comandos SQL

Executar SQL
docker exec -it db-postgres psql -U postgres -d postgres

curl --location 'http://localhost:1026/v2/subscriptions/' \
--header 'Content-Type: application/json' \
--header 'fiware-service: openiot' \
--header 'fiware-servicepath: /airQuality' \
--data '{
  "description": "Notify Cygnus of all context changes",
  "subject": {
    "entities": [
      {
        "idPattern": ".*"
      }
    ]
  },
  "notification": {
    "http": {
      "url": "http://cygnus:5055/notify"
    }
  },
  "throttling": 5
}'


SELECT table_schema,table_name
FROM information_schema.tables
WHERE table_schema ='openiot'
ORDER BY table_schema,table_name;

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'openiot' AND table_name = 'airquality_paxcounter_loradevice';


SELECT * FROM airquality_paxcounter_loradevicelimit 10;


SELECT 
    recvtime::timestamp AS "time",   -- Cast 'recvtime' to a timestamp
    attrvalue::numeric AS "Number"  -- Cast 'attrvalue' to numeric
FROM 
    openiot.airquality_paxcounter_loradevice
WHERE 
    attrtype = 'Number'             -- Filter where 'attrtype' is 'Number'
    AND attrvalue::numeric = 0;     -- Cast 'attrvalue' to numeric before comparison

