## Para deletar dispositivo
```bash
docker exec -it <id_container_mongodb> mongo
```
### No Shel do MongoDb

```bash
show dbs
```

```bash
use iotagentlora
```
```bash
show collections
```
Resulta na seguinte saída
```console
devices
groups
```
### Para ver os dispositivos
```bash
db.devices.find().pretty()
```
### Para deletar uma coleção
```bash
db.<nome_da_collection>.drop()
```
### Para deletar dispositivo
```bash
db.devices.deleteOne({ device_id: "env2" })
```
### Busca por device ID
Você pode buscar por um campo específico, como device_id:
```bash
db.devices.find({ device_id: "tbeam-v1" }).pretty()
```
