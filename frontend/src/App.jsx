import { useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles, Music4 } from "lucide-react";
import IntroScreen from "./components/IntroScreen";

function App() {
  const [script, setScript] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);
  const [started, setStarted] = useState(false);
  const analyzeMood = async () => {
    if (!script.trim()) {
      alert("Please enter a story.");
      return;
    }

    try {
      setLoading(true);
      setResult(null);

      const res = await axios.post(
        "http://127.0.0.1:8000/analyze-mood-premium",
        {
          paragraph: script,
        }
      );

      setResult(res.data);
    } catch (err) {
      console.error(err);

      alert(
        err.response?.data?.detail ||
          "Failed to analyze mood."
      );
    } finally {
      setLoading(false);
    }
  };

  const emotionColors = {
    Joy: "from-yellow-400 to-orange-500",
    Romantic: "from-pink-500 to-purple-600",
    Sadness: "from-blue-500 to-cyan-600",
    Fear: "from-slate-700 to-black",
    Suspense: "from-red-500 to-rose-700",
    Calm: "from-cyan-400 to-blue-500",
    Anger: "from-red-600 to-orange-600",
    Neutral: "from-slate-600 to-slate-800",
  };
  if (!started) {
  return (
    <IntroScreen
      onStart={() => setStarted(true)}
    />
  );
}
  return (
    <div className="min-h-screen bg-slate-950 relative overflow-hidden">

      {/* Background Blobs */}
      <div className="absolute top-20 left-20 w-72 h-72 bg-purple-600/20 rounded-full blur-3xl"></div>

      <div className="absolute bottom-20 right-20 w-72 h-72 bg-cyan-600/20 rounded-full blur-3xl"></div>

      <div className="relative z-10 max-w-6xl mx-auto px-6 py-16">

        {/* HERO */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-12"
        >
          <div className="flex justify-center mb-4">
            <Music4
              size={50}
              className="text-cyan-400"
            />
          </div>

          <h1 className="text-7xl font-extrabold bg-gradient-to-r from-cyan-400 to-purple-500 bg-clip-text text-transparent">
            MediosLink
          </h1>

          <p className="text-slate-400 mt-4 text-xl">
            Every Story Has A Soundtrack
          </p>
        </motion.div>

        {/* INPUT CARD */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          className="
          bg-white/5
          backdrop-blur-xl
          border border-white/10
          rounded-3xl
          p-8
          shadow-2xl
          "
        >
          <textarea
            value={script}
            onChange={(e) =>
              setScript(e.target.value)
            }
            placeholder="Write your narrative..."
            className="
            w-full
            h-72
            bg-slate-900/60
            border border-slate-700
            rounded-2xl
            p-6
            text-white
            resize-none
            outline-none
            text-lg
            "
          />

          <div className="flex justify-between mt-4 text-slate-400 text-sm">
            <span>
              Words:{" "}
              {
                script
                  .trim()
                  .split(/\s+/)
                  .filter(Boolean).length
              }
            </span>

            <span>
              Characters: {script.length}
            </span>
          </div>

          <button
            onClick={analyzeMood}
            disabled={loading}
            className="
            mt-8
            px-10
            py-4
            rounded-2xl
            font-bold
            text-white
            bg-gradient-to-r
            from-violet-600
            to-fuchsia-600
            hover:scale-105
            transition-all
            duration-300
            "
          >
            {loading
              ? "🎭 Analyzing Story..."
              : "Analyze Mood"}
          </button>
        </motion.div>

        {/* RESULTS */}
        <AnimatePresence>
          {result && (
            <motion.div
              initial={{
                opacity: 0,
                y: 40,
              }}
              animate={{
                opacity: 1,
                y: 0,
              }}
              exit={{
                opacity: 0,
              }}
              className={`
              mt-10
              rounded-3xl
              p-8
              text-white
              bg-gradient-to-r
              ${
                emotionColors[
                  result.data
                    .dominant_emotion
                ] ||
                emotionColors.Neutral
              }
              `}
            >
              <div className="flex items-center gap-3 mb-6">
                <Sparkles />
                <h2 className="text-5xl font-bold">
                  {
                    result.data
                      .dominant_emotion
                  }
                </h2>
              </div>

              <div className="grid md:grid-cols-2 gap-4">

                <MetricCard
                  title="Valence"
                  value={
                    result.data.valence
                  }
                />

                <MetricCard
                  title="Arousal"
                  value={
                    result.data.arousal
                  }
                />

                <MetricCard
                  title="Tempo"
                  value={
                    result.data
                      .tempo_preference
                  }
                />

                <MetricCard
                  title="Transition"
                  value={
                    result.data
                      .transition_detected
                      ? "Yes"
                      : "No"
                  }
                />

              </div>

              <div className="mt-8 bg-black/20 rounded-2xl p-5">
                <h3 className="font-bold text-xl mb-3">
                  🧠 AI Narrative Insight
                </h3>

                <p>
                  {
                    result.data
                      .linguistic_justification
                  }
                </p>
              </div>
            </motion.div>
          )}
        </AnimatePresence>
      </div>
    </div>
  );
}

function MetricCard({
  title,
  value,
}) {
  return (
    <div className="bg-white/10 rounded-2xl p-5 backdrop-blur-lg">
      <h3 className="text-sm opacity-70">
        {title}
      </h3>

      <p className="text-3xl font-bold mt-2">
        {value}
      </p>
    </div>
  );
}

export default App;

