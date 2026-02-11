import axios from "axios";

const BASE_URL = "http://127.0.0.1:5000/api";

export const fetchPrices = async () => {
  const response = await axios.get(`${BASE_URL}/prices`);
  return response.data;
};

export const fetchEvents = async () => {
  const response = await axios.get(`${BASE_URL}/events`);
  return response.data;
};

export const fetchChangePoints = async () => {
  const response = await axios.get(`${BASE_URL}/change_points`);
  return response.data;
};

export const fetchRegimeMeans = async () => {
  const response = await axios.get(`${BASE_URL}/regime_means`);
  return response.data;
};
