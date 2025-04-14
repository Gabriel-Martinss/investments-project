import axios from "axios";

const api = axios.create({
  baseURL: "/api",
});

export default {
  // Endpoints de taxas
  getCurrentRates: () => api.get("/rates/current"),
  getInvestmentRates: () => api.get("/rates/investments"),

  // Endpoints de simulação
  runDirectSimulation: (data) => api.post("/simulate/direct", data),
  runInverseSimulation: (data) => api.post("/simulate/inverse", data),
};
