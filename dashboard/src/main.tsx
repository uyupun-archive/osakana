import { render } from 'preact';
import { Home } from './pages/home/home.tsx';
import './index.css';

render(<Home />, document.getElementById('app') as HTMLElement);
