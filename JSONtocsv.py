
import json
import csv

def json_to_csv(json_data, output_file='output.csv'):
    with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
        fieldnames = ['Nombre', 'Empresa', 'Correo', 'Telefono', 'Resumen', 'Pregunta', 'Respuesta']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        info = json_data['info']
        resumen = json_data['resumen_interaccion']
        
        preguntas_booleanas = json_data['preguntas_booleanas']
        preguntas_string = json_data['preguntas_string']
        preguntas_porcentaje = json_data['preguntas_porcentaje']
        
        preguntas = preguntas_booleanas + preguntas_string + preguntas_porcentaje

        for pregunta in preguntas:
            row = {
                'Nombre': info['nombre'],
                'Empresa': info['empresa'],
                'Correo': info['correo'],
                'Telefono': info['telefono'],
                'Resumen': resumen,
                'Pregunta': pregunta['pregunta'],
                'Respuesta': pregunta['respuesta']
            }
            writer.writerow(row)




def extract_data(message):
    response_start = message.find("RESPONSE") + len("RESPONSE")
    response_end = message.find("DATA-JSON")

    response_text = message[response_start:response_end].strip()

    json_start = message.find("{", response_end)
    json_end = message.rfind("}") + 1
    json_text = message[json_start:json_end]

    # Reemplazar los caracteres de nueva línea con espacios en el texto JSON
    json_text = json_text.replace("\n", " ")

    json_data = json.loads(json_text)

    return response_text, json_data

def main():
    message = """RESPONSE
-------------
¡Hola! 😊 Gracias por contactarnos. Nuestros Hemp Wraps de Soulblime
tienen varias ventajas en comparación con otros blunts en el mercado.
Son de primera calidad y 100% orgánicos, sin tabaco, sin nicotina,
veganos y libres de GMO 🌱🌍. Además, ofrecemos una gran variedad de
sabores deliciosos en nuestras líneas Tropical, Frutal y Sweet 🍍🍇🍫.

Además, nuestra marca representa una experiencia única y aventurera en
el mundo del fumar. Visita nuestra página web www.soulblime.com para
conocer más sobre nuestros productos y nuestra marca. También puedes
seguirnos en Instagram @soulblime.oficial para mantenerte actualizado
con nuestras novedades 📱. ¿Hay algo más en lo que podamos ayudarte? ✨

------------------
DATA-JSON
{
  "info": {
    "nombre": "max mardones",
    "empresa": "",
    "correo": "maximiliano.mardones@gmail.com",
    "telefono": ""
  },
  "preguntas_booleanas": [
    {
      "pregunta": "el cliente menciono a la competencia?",
      "respuesta": true
    }
  ],
  "preguntas_string": [
    {
      "pregunta": "cual es el estado de animo del cliente",
      "respuesta": "curioso"
    }
  ],
  "preguntas_porcentaje": [
    {
      "pregunta": "que tan propenso o interesado esta en soulblime?
SIENDO UN 100% QUe lo va a comprar",
      "respuesta": 60
    }
  ],
  "resumen_interaccion": "El cliente preguntó sobre las ventajas de
los Hemp Wraps de Soulblime en comparación con la competencia. Se le
proporcionaron detalles sobre la calidad, ingredientes y sabores
ofrecidos por Soulblime."
}
"""
    
    response_text, json_data = extract_data(message)
    #print("RESPONSE:")
    print(response_text)
    #print("\nDATA-JSON:")
    print(json.dumps(json_data, indent=2))
    json_to_csv(json_data)

if __name__ == "__main__":
    main()
