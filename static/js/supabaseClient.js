import { createClient } from 'https://cdn.jsdelivr.net/npm/@supabase/supabase-js/+esm'

const supabaseUrl = 'https://wtphpixmudjbcsnsgmrb.supabase.co'
const supabaseAnonKey = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6Ind0cGhwaXhtdWRqYmNzbnNnbXJiIiwicm9sZSI6ImFub24iLCJpYXQiOjE3NzAxMDQ1OTgsImV4cCI6MjA4NTY4MDU5OH0.rTyb4WW2L8dXmr8RyxgWcUc0ONa2Gv972Pa8UkGAoro'

export const supabase = createClient(supabaseUrl, supabaseAnonKey)

