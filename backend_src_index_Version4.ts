import express from "express";
import cors from "cors";
import helmet from "helmet";
import morgan from "morgan";
import { agenticRoutes } from "./routes/agentic";

const app = express();
app.use(helmet());
app.use(cors());
app.use(morgan("tiny"));
app.use(express.json({ limit: "50mb" }));
app.use(express.raw({ type: "application/octet-stream", limit: "50mb" }));

app.use("/api/agentic", agenticRoutes);

app.listen(4000, () => console.log("Virtual Expediter backend running on 4000"));