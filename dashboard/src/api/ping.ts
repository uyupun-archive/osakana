import axios from 'axios';

import type { PingResponse } from '../types/ping';
import { isValidPingResponse } from '../types';

export const ping = async (): Promise<PingResponse> => {
  const res = await axios.get('/api/ping');
  if (isValidPingResponse(res.data)) {
    return res.data;
  }
  throw new PingTypeError();
};

class PingTypeError extends Error {
  constructor() {
    const message = "Ping type error";
    super(message);
    this.name = 'PingTypeError';
    Object.setPrototypeOf(this, new.target.prototype);
  };
};
