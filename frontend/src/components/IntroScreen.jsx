import { motion } from "framer-motion";
import { useEffect, useState } from "react";

import clapper from "../assets/clapperboard.png";
import introMusic from "../assets/intro.mp3";
import cinemaBg from "../assets/cinema-bg.jpg";

export default function IntroScreen({ onStart }) {
  const [introFinished, setIntroFinished] =
    useState(false);

  const [showTitle, setShowTitle] =
    useState(false);

  useEffect(() => {

    const audio = new Audio(
      introMusic
    );

    audio.volume = 0.7;

    audio.play().catch(() => {});

    setTimeout(() => {
      setShowTitle(true);
    }, 5000);

    setTimeout(() => {
      setIntroFinished(true);
    }, 12000);

    return () => {
      audio.pause();
    };

  }, []);

  return (
    <div className="h-screen relative overflow-hidden bg-black">

      {/* Moving Cinema Background */}

      <motion.div
        className="absolute inset-0 opacity-25"
        animate={{
          y: ["0%", "-50%"]
        }}
        transition={{
          duration: 30,
          repeat: Infinity,
          ease: "linear"
        }}
      >
        <img
          src={cinemaBg}
          className="w-full"
          alt=""
        />

        <img
          src={cinemaBg}
          className="w-full"
          alt=""
        />
      </motion.div>

      {/* Dark Overlay */}

      <div className="absolute inset-0 bg-black/75" />

      {/* Content */}

      <div className="relative z-10 h-full flex flex-col items-center justify-center">

        {/* Clapperboard */}

        <motion.img
          src={clapper}
          alt="clapperboard"

          initial={{
            opacity: 0,
            scale: 0.5,
            y: 100,
            filter: "blur(10px)"
          }}

          animate={{
            opacity: 1,
            scale: 1,
            y: 0,
            filter: "blur(0px)"
          }}

          transition={{
            duration: 12,
            ease: "easeOut"
          }}

          className="
            w-[450px]
            mx-auto
            drop-shadow-[0_0_40px_rgba(255,255,255,0.4)]
          "
        />

        {/* Title */}

        {showTitle && (

          <motion.div
            className="text-center"

            initial={{
              opacity: 0,
              y: 50
            }}

            animate={{
              opacity: 1,
              y: 0
            }}

            transition={{
              duration: 2
            }}
          >

            <h1 className="text-white text-7xl font-extrabold mt-6">
              MediosLink
            </h1>

            <p className="text-zinc-300 mt-3 text-xl">
              Every Story Has A Soundtrack
            </p>

          </motion.div>

        )}

        {/* Button */}

        {introFinished && (

          <motion.button

            initial={{
              opacity: 0,
              scale: 0.8
            }}

            animate={{
              opacity: 1,
              scale: 1
            }}

            onClick={onStart}

            className="
              mt-8
              px-8
              py-4
              rounded-2xl
              bg-white
              text-black
              font-bold
              hover:scale-105
              transition-all
              shadow-2xl
            "
          >
            Enter Experience
          </motion.button>

        )}

      </div>

    </div>
  );
}

