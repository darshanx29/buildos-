-- ============================================
--  BuildOS — Supabase SQL Schema
--  Paste this into Supabase SQL Editor and run
-- ============================================

-- Projects table
create table projects (
  id uuid default gen_random_uuid() primary key,
  name text not null,
  site_location text,
  budget numeric(12,2) not null default 0,
  created_at timestamptz default now()
);

-- Materials table
create table materials (
  id uuid default gen_random_uuid() primary key,
  project_id uuid references projects(id) on delete cascade,
  name text not null,
  unit text not null default 'bags',
  quantity numeric(10,2) not null default 0,
  unit_price numeric(10,2) not null default 0,
  reorder_threshold numeric(10,2) not null default 10,
  created_at timestamptz default now()
);

-- Transactions table (every stock movement)
create table transactions (
  id uuid default gen_random_uuid() primary key,
  material_id uuid references materials(id) on delete cascade,
  project_id uuid references projects(id) on delete cascade,
  type text check (type in ('in','out')) not null,
  quantity numeric(10,2) not null,
  note text,
  logged_by text default 'engineer',
  created_at timestamptz default now()
);

-- Invoices table
create table invoices (
  id uuid default gen_random_uuid() primary key,
  project_id uuid references projects(id) on delete cascade,
  invoice_number text not null,
  status text check (status in ('draft','sent','paid')) default 'draft',
  total_amount numeric(12,2) default 0,
  created_at timestamptz default now()
);

-- Invoice line items
create table invoice_items (
  id uuid default gen_random_uuid() primary key,
  invoice_id uuid references invoices(id) on delete cascade,
  material_id uuid references materials(id),
  description text not null,
  quantity numeric(10,2) not null,
  unit_price numeric(10,2) not null,
  total numeric(12,2) generated always as (quantity * unit_price) stored
);

-- ─── Seed Demo Data ───────────────────────────────────────

insert into projects (name, site_location, budget) values
  ('Andheri Tower Block A', 'Andheri East, Mumbai', 2500000),
  ('Pune Highway Bridge', 'Pune-Mumbai Expressway', 5000000);

insert into materials (project_id, name, unit, quantity, unit_price, reorder_threshold)
select id, 'Cement (OPC 53)',    'bags',      320,   450,  50   from projects where name = 'Andheri Tower Block A'
union all
select id, 'Steel Rebar (12mm)', 'kg',        8500,  85,   500  from projects where name = 'Andheri Tower Block A'
union all
select id, 'River Sand',         'cubic ft',  420,   55,   100  from projects where name = 'Andheri Tower Block A'
union all
select id, 'Bricks (Red)',       'units',     12000, 8,    2000 from projects where name = 'Andheri Tower Block A'
union all
select id, 'Cement (OPC 53)',    'bags',      18,    450,  50   from projects where name = 'Pune Highway Bridge'
union all
select id, 'Steel Rebar (16mm)', 'kg',        5200,  92,   300  from projects where name = 'Pune Highway Bridge';
