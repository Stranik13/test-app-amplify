import { useEffect, useState } from 'react'
import { API } from 'aws-amplify'

import logo from './logo.svg'
import './App.css'

function App () {
  const [songs, setSongs] = useState([])

  useEffect(() => {
    const getData = async () => {
      const data = await API.get('britneySongApi', '/song/')
      setSongs(data.data.Items)

      // const data2 = await API.del('britneySongApi', '/song/30325cd8-2c96-4bf8-a4b8-1e0f289940b5')
      // console.log(data2)

      // const data2 = await API.post('britneySongApi', '/song/', { body: { name: 'Everytime', year: '2003', link: 'https://www.youtube.com/watch?v=8YzabSdk7ZA' } })
      // console.log(data2)

      // const data = await API.put('britneySongApi', '/song/a7795231-7de8-4d2a-8ca8-44bd8cef8eae', { body: { song_name: 'Toxicity', year: '2004', link: 'https://www.youtube.com/watch?v=LOZuxwVk7TU' } })
      // console.log(data)
    }

    getData()
  }, [])
  return (
    <div className='App'>
      <h1 className='pink-text'>✨Britney Spears Songs✨</h1>
      {songs.map(song => (
        <div key={song.id.S}>
          <h2>{song.name.S}</h2>
          <iframe width='560' height='315' src={song.link.S.replace('watch?v=', 'embed/')} frameBorder='0' allow='accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture' allowFullScreen />
        </div>
      ))}
    </div>
  )
}

export default App
