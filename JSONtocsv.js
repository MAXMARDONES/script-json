
// jsonToCsv.js
import fs from 'fs';
import { parse } from 'json2csv';

export const jsonToCsv = (json_data, output_file = 'output.csv') => {
  const fieldnames = ['Nombre', 'Empresa', 'Correo', 'Telefono', 'Resumen', 'Pregunta', 'Respuesta'];
  const info = json_data['info'];
  const resumen = json_data['resumen_interaccion'];
  const preguntas_booleanas = json_data['preguntas_booleanas'];
  const preguntas_string = json_data['preguntas_string'];
  const preguntas_porcentaje = json_data['preguntas_porcentaje'];
  const preguntas = [...preguntas_booleanas, ...preguntas_string, ...preguntas_porcentaje];

  const csvData = preguntas.map(pregunta => ({
    Nombre: info['nombre'],
    Empresa: info['empresa'],
    Correo: info['correo'],
    Telefono: info['telefono'],
    Resumen: resumen,
    Pregunta: pregunta['pregunta'],
    Respuesta: pregunta['respuesta']
  }));

  const csv = parse(csvData, { fields: fieldnames });
  fs.writeFileSync(output_file, csv, 'utf-8');
};

// extractData.js
export const extractData = (message) => {
  const response_start = message.indexOf("RESPONSE") + "RESPONSE".length;
  const response_end = message.indexOf("DATA-JSON");

  const response_text = message.slice(response_start, response_end).trim();

  const json_start = message.indexOf("{", response_end);
  const json_end = message.lastIndexOf("}") + 1;
  const json_text = message.slice(json_start, json_end).replace("\n", " ");

  const json_data = JSON.parse(json_text);

  return { responseText: response_text, jsonData: json_data };
};

// main.js
import { jsonToCsv } from './jsonToCsv';
import { extractData } from './extractData';

const main = () => {
  const message = "Here goes the message";
  const { responseText, jsonData } = extractData(message);

  console.log(responseText);
  console.log(JSON.stringify(jsonData, null, 2));
  jsonToCsv(jsonData);
};

main();
```

Luego puedes importar y usar `jsonToCsv` y `extractData` en tu componente Next.js de la siguiente manera:

```javascript
import { jsonToCsv, extractData } from './utils';

// Luego puedes usar las funciones dentro de tu componente o donde sea necesario
