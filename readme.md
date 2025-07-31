# 📵 Generador de Blacklist para llamadas spam (YACB) (Solo España)

Este proyecto contiene un script en Python que genera automáticamente una lista de bloqueo personalizada para **Yet Another Call Blocker** (YACB), una app de código abierto para Android que permite bloquear llamadas por patrón de número.

---

## 📱 Aplicación necesaria

Debes instalar **Yet Another Call Blocker**, disponible en F-Droid:

🔗 [Descargar desde F-Droid](https://f-droid.org/en/packages/dummydomain.yetanothercallblocker/)

También puedes consultar este foro de XDA para saber cómo configurarla y cargar listas personalizadas:

🔗 [XDA Forums: Android – Bloquear rangos de llamadas](https://xdaforums.com/t/android-how-to-block-several-or-range-based-phone-callers-numbers.4638624/)

Repositorio oficial (código fuente):  
🔗 [YACB en GitLab](https://gitlab.com/xynngh/YetAnotherCallBlocker)

---

## 💡 ¿Para qué sirve este script?

Aunque YACB ya viene con su **propia base de datos de números sospechosos y spam**, este script pretende ir **un paso más allá**:

🔍 Analiza directamente la base de datos de numeración geográfica oficial de la **CNMC (España)** para detectar los rangos telefónicos asignados a operadores que suelen ser utilizados para hacer llamadas comerciales agresivas o directamente fraudulentas.

🎯 Así, puedes generar una lista de bloqueo que **filtra todos los números fijos sospechosos**, incluso aunque aún no aparezcan en bases de datos de spam.

---

## 🚫 Qué bloquea exactamente

El script genera una lista de bloqueo que incluye:

- Todos los rangos asignados a **AIRE NETWORKS DEL MEDITERRÁNEO, S.L.**
- Todos los rangos de **ORANGE ESPAGNE, S.A. UNIPERSONAL**, personalizable con **exclusión de provincias de donde el usuario pueda recibir llamadas legítimas**, como por ejemplo:
  ```python
  PROVINCIAS_EXCLUIDAS_ORANGE = {"Madrid", "Barcelona"}
  ```

✏️ Puedes modificar esa línea en el script para **ajustarlo a tus propias necesidades**, manteniendo o eliminando provincias en función de si esperas llamadas legítimas desde ellas.

---

## ⚠️ Aviso importante

- El script **solo bloquea números fijos españoles**.
- Se basa en patrones amplios (ej. `822**`, `+34822**`), por lo que puede **bloquear llamadas legítimas** dentro de esos rangos.
- No bloquea móviles ni llamadas VoIP extranjeras.
- El usuario es responsable de revisar o ajustar el filtrado antes de importar la lista en YACB.

---

## 🧰 ¿Qué hace el script?

1. Descarga automáticamente el fichero actualizado de numeración de la CNMC desde:
   ```
   https://numeracionyoperadores.cnmc.es/
   ```
2. Extrae y analiza el fichero `geograficos.txt`.
3. Filtra los rangos por operador y provincia según lo descrito arriba.
4. Genera un fichero `.csv` compatible con YACB en este formato:
   ```
   ID,name,pattern,creationTimestamp,numberOfCalls,lastCallTimestamp
   1,Spam822,+34822**,1698437458896,0,
   2,Spam822,822**,1698437458896,0,
   ...
   ```
5. El archivo se guarda automáticamente con nombre `blacklist-DD-MM-YYYY.csv`.

---

## ✅ Usar el CSV directamente

Este repositorio incluye un CSV ya generado (`blacklist-XX-XX-XXXX.csv`) para quien quiera usarlo sin ejecutar el script.

### Instrucciones para importar en YACB:

1. Copia el archivo `.csv` al almacenamiento del teléfono.
2. Abre YACB > Ajustes > Importar lista.
3. Selecciona el archivo desde tu gestor de archivos.
4. Activa la protección desde la pantalla principal.

---

## 💻 Ejecutar el script

### Requisitos:
- Python 3
- Dependencias:
  ```bash
  pip install requests
  ```

### Ejecución:
```bash
python blacklist_form_cnmc.py
```

El CSV aparecerá en el mismo directorio con el nombre `blacklist-DD-MM-YYYY.csv`.

---

## 🛠 Personalización

Puedes editar el script para:
- Incluir o excluir operadores.
- Cambiar las provincias excluidas.
- Adaptar el formato de salida.

---

## 🤝 Contribuciones

¿Conoces más operadores que deberían bloquearse? ¿Nuevos rangos? ¿Ideas de mejora? Puedes abrir una issue o PR.

---

## 📜 Licencia

El contenido de este proyecto se publica con la intención de ayudar a usuarios a protegerse contra el spam telefónico. Úsalo de forma responsable y ajústalo según tus necesidades.
