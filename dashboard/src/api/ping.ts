import axios from 'axios';

export const ping = async () => {
  const res = await axios.get('/api/ping');
  return res.data;
};
