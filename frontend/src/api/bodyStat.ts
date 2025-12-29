import { api } from "./client";

export type BodyStatCreate = {
  user_id: number;
  measured_at: string; // YYYY-MM-DD
  body_weight: number;
  notes?: string | null;
};

export type BodyStat = {
  id: number;
  user_id: number;
  measured_at: string; // "YYYY-MM-DD"
  body_weight: number;
  body_weight_goal?: number | null;
  body_fat_percentage?: number | null;
  notes?: string | null;
  created_at: string;
};

export async function createBodyStat(payload: BodyStatCreate) {
  const response = await api.post("/body-stats", payload);
  return response.data;
}

export async function getBodyStatsByUser(userId: number) {
  const res = await api.get<BodyStat[]>(`/body-stats/user/${userId}`);
  return res.data;
}
