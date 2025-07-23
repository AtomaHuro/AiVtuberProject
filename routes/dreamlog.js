const express = require('express');
const fs = require('fs');
const path = require('path');
const router = express.Router();

const LOG_PATH = path.join(__dirname, '..', 'memory', 'dream_log.json');

router.get('/api/dreamlog', (req, res) => {
  fs.readFile(LOG_PATH, 'utf8', (err, data) => {
    if (err) {
      return res.status(500).json({ error: 'Could not read dream log.' });
    }
    try {
      const parsed = JSON.parse(data);
      res.json(parsed);
    } catch (e) {
      res.status(500).json({ error: 'Malformed dream log JSON.' });
    }
  });
});

module.exports = router;
