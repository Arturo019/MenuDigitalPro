/**
 * Comprueba si hay usuario de Supabase logueado.
 * Si no hay sesión, redirige a /login.
 * Usado en inicio.html, mis_cartas.html y otras páginas protegidas.
 */
import { supabase } from '/static/js/supabaseClient.js';

export async function checkAuth() {
  const { data: { user } } = await supabase.auth.getUser();
  if (!user) {
    window.location.href = '/login';
  }
}
