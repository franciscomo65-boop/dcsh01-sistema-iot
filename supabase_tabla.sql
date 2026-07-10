-- Ejecutar esto en el SQL Editor de Supabase para crear la tabla de eventos

create table eventos (
  id bigint generated always as identity primary key,
  dispositivo text not null,
  led text not null,
  estado text not null,
  timestamp timestamptz not null default now()
);

-- Permite insertar filas usando la API key publica (anon)
alter table eventos enable row level security;

create policy "permitir insertar eventos"
on eventos
for insert
to anon
with check (true);

create policy "permitir leer eventos"
on eventos
for select
to anon
using (true);
