const express = require('express');
const bodyParser = require('body-parser');
const fs = require('fs');
const path = require('path');
const { exec } = require('child_process');

const app = express();
const tempDir = path.join(__dirname, 'temp');

// Crear directorio temporal si no existe
if (!fs.existsSync(tempDir)) fs.mkdirSync(tempDir);

app.use(express.static('public'));
app.use(bodyParser.json());

app.post('/run', (req, res) => {
    const userCode = req.body.code;
    const userInput = req.body.input;

    // Validar el nombre de la clase pública
    const match = userCode.match(/public\s+class\s+(\w+)/);
    if (!match) {
        return res.json({ success: false, error: 'No se encontró una clase pública en el código' });
    }

    const className = match[1];
    const userDir = path.join(tempDir, `session-${Date.now()}`);
    fs.mkdirSync(userDir);

    const filePath = path.join(userDir, `${className}.java`);
    const inputFilePath = path.join(userDir, 'input.txt');

    // Guardar archivos temporales
    fs.writeFileSync(filePath, userCode);
    fs.writeFileSync(inputFilePath, userInput);

    // Comando para compilar y ejecutar
    const command = `javac "${filePath}" && java -cp "${userDir}" ${className} < "${inputFilePath}"`;

    exec(command, (error, stdout, stderr) => {
        // Eliminar archivos temporales
        fs.rmSync(userDir, { recursive: true, force: true });

        if (error) {
            res.json({ success: false, error: stderr || 'Error ejecutando el código' });
        } else {
            res.json({ success: true, output: stdout.trim() });
        }
    });
});

app.listen(3000, () => {
    console.log('Servidor corriendo en http://localhost:3000');
});
