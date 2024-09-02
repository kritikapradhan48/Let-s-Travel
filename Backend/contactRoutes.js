const express = require('express');
const Contact = require('../models/Contact');

const router = express.Router();

// Submit contact form
router.post('/', async (req, res) => {
  const { name, email, message } = req.body;

  try {
    const contact = new Contact({
      name,
      email,
      message,
    });

    await contact.save();

    res.json({ msg: 'Message received, thank you!' });
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
