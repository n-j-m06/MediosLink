import { useState } from "react";
import axios from "axios";
import { motion, AnimatePresence } from "framer-motion";
import { Sparkles } from "lucide-react";
import IntroScreen from "./components/IntroScreen";
import cinemaVideo from "./assets/cinema-bg.mp4";

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

  const emotionIcons = {
  Joy: "✨",
  Romantic: "❤️",
  Sadness: "💙",
  Fear: "😨",
  Suspense: "🎭",
  Calm: "🌊",
  Anger: "🔥",
  Neutral: "🎵",
};
  if (!started) {
  return (
    <IntroScreen
      onStart={() => setStarted(true)}
    />
  );
}
  return (
   <div className="min-h-screen relative overflow-hidden">
    {/* Video Background */}

<video
  autoPlay
  loop
  muted
  playsInline
  className="
    absolute
    inset-0
    w-full
    h-full
    object-cover
  "
>
  <source
    src={cinemaVideo}
    type="video/mp4"
  />
</video>

{/* Dark Overlay */}

<div className="absolute inset-0 bg-black/55" />

      {/* Background Blobs */}

      <div className="relative z-10 max-w-7xl mx-auto px-8 pt-12">

        {/* HERO */}
        <motion.div
          initial={{ opacity: 0, y: -30 }}
          animate={{ opacity: 1, y: 0 }}
          className="text-center mb-6"
        >

        <h1
  className="
  text-8xl
  font-black
  tracking-tight
  text-white
  drop-shadow-[0_0_30px_rgba(255,255,255,0.2)]
  "
>
            MediosLink
          </h1>

         <p
  className="
  text-slate-300
  mt-3
  text-lg
  tracking-[0.3em]
  uppercase
  "
>
            Every Story Has A Soundtrack
          </p>
        </motion.div>
      <div
  className="
  flex
  items-center
  justify-center
  gap-8
  mt-4
  "
>

  <div
    className="
    w-16
    h-[2px]
    bg-cyan-400
    rounded-2xl
    "
  />

  <div
    className="
    w-16
    h-[2px]
    bg-purple-500
    rounded-full
    "
  />

</div>
        {/* INPUT CARD */}
{/* STORY STUDIO */}

<motion.div
  initial={{ opacity: 0 }}
  animate={{ opacity: 1 }}
  className="max-w-6xl mx-auto"
>

  <div
  className="
  bg-black/25
  backdrop-blur-xl
    border border-white/10
    rounded-[32px]
    overflow-hidden
    shadow-[0_0_50px_rgba(0,0,0,0.4)]
    "
  >

    {/* Header */}

    

     

    {/* Text Area */}

    <textarea
      value={script}
      onChange={(e) =>
        setScript(e.target.value)
      }
      placeholder="Begin your story..."
      className="
      w-full
      h-[300px]
      bg-transparent
      p-8
      placeholder:text-slate-500
      font-mono
      text-white
      text-xl
      leading-relaxed
      resize-none
      outline-none
      "
    />

    {/* Footer */}

    <div
      className="
      flex
      justify-between
      items-center
      px-8
      py-5
      border-t
      border-white/10
      "
    >

      <div className="flex gap-8 text-slate-400">

        <span>
          Words:
          {
            script
              .trim()
              .split(/\s+/)
              .filter(Boolean).length
          }
        </span>

        <span>
          Characters:
          {script.length}
        </span>

      </div>

      <button
        onClick={analyzeMood}
        disabled={loading}
        className="
group
px-8
py-4
rounded-2xl
bg-black/40
border
border-white/20
backdrop-blur-xl
text-white
font-semibold
hover:scale-105
transition-all
duration-300
"
      >
        {loading
          ? "🎭 Reading Story..."
          : "✨ Generate Soundtrack"}
      </button>

    </div>

  </div>

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
             className="
mt-12
max-w-5xl
mx-auto
bg-black/30
backdrop-blur-xl
border
border-white/10
rounded-[32px]
p-10
text-white
shadow-[0_0_40px_rgba(255,255,255,0.05)]
"
            >
              <div className="text-center">

  <div className="text-7xl mb-4">
    {
      emotionIcons[
        result.data
          .dominant_emotion
      ]
    }
  </div>

  <h2
    className="
    text-7xl
    font-black
    tracking-tight
    "
  >
    {
      result.data
        .dominant_emotion
    }
  </h2>

  <p
    className="
    text-slate-400
    mt-3
    uppercase
    tracking-[0.3em]
    "
  >
    Emotion Detected
  </p>

</div>

 <div
  className="
  grid
  md:grid-cols-2
  gap-6
  mt-12
  "
>

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

              <div
  className="
  mt-10
  border-t
  border-white/10
  pt-8
  "
>
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
    <div
      className="
      bg-white/5
      border
      border-white/10
      rounded-3xl
      p-6
      backdrop-blur-xl
      text-center
      "
    >
      <h3
        className="
        text-slate-400
        uppercase
        tracking-widest
        text-sm
        "
      >
        {title}
      </h3>

      <p
        className="
        text-4xl
        font-bold
        text-white
        mt-4
        "
      >
        {value}
      </p>
    </div>
  );
}

export default App;

