import { useState } from "react";
import axios from "axios";

function App() {
  const [script, setScript] = useState("");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const analyzeMood = async () => {
    if (!script.trim()) {
      alert("Please enter some text.");
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
          "Failed to analyze mood. Check backend."
      );
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen bg-slate-950 flex items-center justify-center p-6">
      <div className="w-full max-w-5xl bg-white/5 backdrop-blur-lg border border-white/10 rounded-3xl p-8">

        {/* Header */}
        <h1 className="text-5xl font-bold text-white mb-4">
          MediosLink
        </h1>

        <p className="text-slate-400 mb-8">
          Every Story Has A Soundtrack
        </p>

        {/* Text Area */}
        <textarea
          value={script}
          onChange={(e) => setScript(e.target.value)}
          placeholder="Write your story here..."
          className="w-full h-64 bg-slate-900 text-white rounded-2xl p-5 border border-slate-700 outline-none resize-none"
        />

        {/* Button */}
        <button
          onClick={analyzeMood}
          disabled={loading}
          className="mt-6 px-8 py-3 bg-violet-600 hover:bg-violet-700 text-white rounded-xl font-semibold transition-all duration-300"
        >
          {loading ? "Analyzing..." : "Analyze Mood"}
        </button>

        {/* Results */}
        {result && (
          <div className="mt-8 p-6 rounded-2xl bg-slate-900 text-white border border-slate-700">

            <h2 className="text-3xl font-bold mb-6">
              🎭 {result.data.dominant_emotion}
            </h2>

            <div className="grid grid-cols-2 gap-4">

              <div className="bg-slate-800 p-4 rounded-xl">
                <h3 className="text-slate-400 text-sm mb-1">
                  Valence
                </h3>
                <p className="text-2xl font-semibold">
                  {result.data.valence}
                </p>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl">
                <h3 className="text-slate-400 text-sm mb-1">
                  Arousal
                </h3>
                <p className="text-2xl font-semibold">
                  {result.data.arousal}
                </p>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl">
                <h3 className="text-slate-400 text-sm mb-1">
                  Tempo Preference
                </h3>
                <p className="text-2xl font-semibold">
                  {result.data.tempo_preference}
                </p>
              </div>

              <div className="bg-slate-800 p-4 rounded-xl">
                <h3 className="text-slate-400 text-sm mb-1">
                  Emotional Transition
                </h3>
                <p className="text-2xl font-semibold">
                  {result.data.transition_detected ? "Yes" : "No"}
                </p>
              </div>

            </div>

            <div className="mt-6 bg-slate-800 p-5 rounded-xl">
              <h3 className="text-lg font-semibold mb-3">
                🧠 AI Narrative Insight
              </h3>

              <p className="text-slate-300 leading-relaxed">
                {result.data.linguistic_justification}
              </p>
            </div>

          </div>
        )}
      </div>
    </div>
  );
}

export default App;