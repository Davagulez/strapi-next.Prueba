import Image from 'next/image'
import styles from './page.module.css'
import usePropiedades from "../../hooks/usePropiedades";

export default function Home() {
  const { Propiedades } = usePropiedades();

  return (
   <h1>
      <Propiedades />
   </h1>
  )
}
