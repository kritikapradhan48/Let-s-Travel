const express = require('express');
const Experience = require('../models/Experience');

const router = express.Router();

// Get all experiences
router.get('/', async (req, res) => {
  try {
    const experiences = await Experience.find();
    res.json(experiences);
  } catch (err) {
    console.error(err.message);
    res.status(500).send('Server error');
  }
});

module.exports = router;
