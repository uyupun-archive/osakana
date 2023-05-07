// import { useState } from 'preact/hooks'
import LogoWithText from './assets/logo-with-text.svg'
import './app.css'

export function App() {
  // const [count, setCount] = useState(0)

  return (
    <>
      <img src={LogoWithText} alt="Osakana logo with text" width="500" />
      <div>
				<input type="text" placeholder="https://..." />
				<button type="button">Add</button>
			</div>
      <div>
				<input type="text" placeholder="Keyword" />
				<button type="button">Search</button>
				<button type="button">Feeling</button>
			</div>
      <table border="1">
        <thead>
					<tr>
						<th>Title</th>
						<th>Action</th>
					</tr>
				</thead>
        <tbody>
          <tr>
            <td>
              <a href="https://preactjs.com/tutorial/" target="_blank" rel="noreferrer noopener">TestTestTestTestTest</a>
            </td>
            <td>
              <button type="button" onClick={() => console.log("Read")}>Read</button>
              <button type="button" onClick={() => console.log("Delete")}>Delete</button>
            </td>
          </tr>
				</tbody>
			</table>
    </>
  )
}
