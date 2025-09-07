router.post("/voice", async (req, res) => {
  try {
    const userRole = req.headers["x-user-role"] as string;
    const buffer = Buffer.from(req.body);
    const result = await handleVoiceInput(buffer, userRole);
    res.json(result);
  } catch (err) {
    res.status(400).json({ error: err.message });
  }
});