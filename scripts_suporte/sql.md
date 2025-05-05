## Estudar Fiware com ML

//https://github.com/ging/fiware-ml-supermarket

## Comandos SQL

### Testar cliente SQL
```sh
docker exec -it db-postgres psql -U postgres -d postgres
```


### Comandos SQL para verificar seus dados

```SQL
SELECT table_schema,table_name
FROM information_schema.tables
WHERE table_schema ='openiot'
ORDER BY table_schema,table_name;

SELECT column_name, data_type, is_nullable
FROM information_schema.columns
WHERE table_schema = 'openiot' AND table_name = 'airquality_paxcounter_loradevice';
```

```SQL
SELECT * FROM openiot.airquality_paxcounter_loradevice limit 10;
```

### Comando SQL para gerar gráfico Grafana
```SQL
SELECT 
    recvtime::timestamp AS "time",   
    attrvalue::numeric AS "Number"  
FROM 
    openiot.airquality_paxcounter_loradevice
WHERE 
    attrtype = 'Number'        
    AND attrvalue::numeric = 0;
```
