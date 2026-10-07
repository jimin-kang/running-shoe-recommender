import { useState } from 'react'
import heroImg from './assets/hero.png'
import reactLogo from './assets/react.svg'
import viteLogo from './assets/vite.svg'
import './App.css'
import InputFormPage from './form.tsx'
import NumberSliderForm from './SliderForm.tsx'

function App() {
  const [count, setCount] = useState(0)

  return (
    <>
      <h1>Welcome to your own shoe recommender :) </h1>
      <NumberSliderForm />
    </>
  )
}

export default App
