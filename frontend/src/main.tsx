import './index.css';
import { createRoot } from 'react-dom/client';
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { HomeRoutes, PatientRoutes, ChatRoutes } from './routes';

createRoot(document.getElementById('root')!).render(
  <BrowserRouter>
    <Routes>
      {HomeRoutes}
      {PatientRoutes}
      {ChatRoutes}
      <Route path='*' element={<div>404 Not Found</div>} />
    </Routes>
  </BrowserRouter>,
);
