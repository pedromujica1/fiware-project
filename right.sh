curl localhost:4041/iot/devices -s -S --header 'Content-Type: application/json' --header 'Accept: application/json' --header 'fiware-service: smartgondor' --header 'fiware-servicepath: /gardens' -d @- <<EOF
{
  "devices": [
    {
    
      
      "device_id": "sensores-londrina",
      "entity_name": "LORA-L",
      "entity_type": "LoraDevice"
    
      "attributes": [
        {
           "object_id": "Best_CO",
	   "name": "Best_CO",
	   "type": "Float",
        },
        {
          "object_id": "Best_NO2",
	  "name": "Best_NO2",
	  "type": "Float",
        },
        {
          "object_id": "Best_OX",
          "name": "Best_OX",
          "type": "Float",
       
	},
	{
	  "object_id": "Best_OX",
          "name": "Best_OX",
          "type": "Float", 
	},
	{
	  "object_id": "Best_OX",
          "name": "Best_OX",
          "type": "Float",
	},
	
      ],
      "internal_attributes": {
        "lorawan": {
          "application_server": {
            "host": "au1.cloud.thethings.network:1883",
            "username": "envcity-aqm@ttn",
            "password": "ZA75Y575PUZELIDGHRRLRJOCV4MM465NCAEUICA",
            "provider": "ttn"
          },
          "dev_eui": "70B3D57ED00678EB",
          "app_eui": "1231231231231231",
          "application_id": "envcity-aqm",
          "application_key": "E078A5F764CFA112E6BA26496CA19A5B",
          "data_model": "application_server"
        }
      }
    }
  ]
}
EOF
