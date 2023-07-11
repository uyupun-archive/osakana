import axios from 'axios';

import { PingTypeError } from '../errors';
import { isValidPingResponse, type PingResponse } from '../types';

const apiUrl = import.meta.env.VITE_API_URL;

export const ping = async (): Promise<PingResponse> => {
  const res = await axios.get(`${apiUrl}/api/ping`);
  if (isValidPingResponse(res.data)) {
    return res.data;
  }
  throw new PingTypeError();
};
