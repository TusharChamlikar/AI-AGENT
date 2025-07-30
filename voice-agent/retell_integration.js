const express = require('express');
const bodyParser = require('body-parser');
const axios = require('axios');

const app = express();
app.use(bodyParser.json());

app.post('/retell', async (req, res) => {
    const { name, amount, due_date } = req.body;

    const response = await axios.post("http://localhost:8000/reminder", {
        name, amount, due_date
    });

    res.send({ speechText: response.data.reminder });
});

app.listen(3000, () => console.log("Retell AI webhook listening"));
