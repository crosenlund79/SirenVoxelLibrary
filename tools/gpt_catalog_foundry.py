#!/usr/bin/env python3
"""GPT Sirens Asset Foundry: independent procedural editable VOX candidates.
Generates actual MagicaVoxel VOX 150 files and PNG previews from the occupied voxels.
Uses no assets or modeling scripts from Claude's namespace.
"""
from __future__ import annotations
import json, math, os, random, struct, sys
from collections import defaultdict
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

PALETTE_HEX={
 'shadow':'252A2B','charcoal':'363C3D','steel':'687072','highlight':'ADB4B2','concrete':'90918A','plaster':'CCC5B6',
 'lightwood':'BC9670','wood':'967455','darkwood':'5E4839','green':'566C60','olive':'777B55','brick':'9A594B',
 'rust':'B36E44','slate':'687A82','cloth':'D7CDB9','blue':'697D8B','black':'171E21','bone':'E7DCC7',
 'yellow':'D8B66E','glass':'7B9597','skin':'BD9B83','soil':'514E43','leaf':'6F7C60','white':'F3EEE0'}
P={k:i+1 for i,k in enumerate(PALETTE_HEX)}
RGB={i+1:tuple(bytes.fromhex(v)) for i,v in enumerate(PALETTE_HEX.values())}

MANIFEST={
 'furniture': '''
sofa sofa 2.4,.95,.88; armchair sofa .92,.92,.92; coffee_table table 1.15,.62,.46; television screen 1.08,.15,.68; tv_cabinet cabinet 1.7,.45,.62; bookshelf shelf 1.25,.4,1.85; side_table table .56,.52,.54; floor_lamp lamp .4,.4,1.67; small_storage_cabinet cabinet .95,.46,1.1; rug rug 2.4,1.75,.06; stool stool .43,.43,.7; sideboard cabinet 1.75,.49,.87; small_shelf shelf .83,.34,1.23; single_bed bed 1.05,2.06,.82; double_bed bed 1.74,2.08,.88; nightstand cabinet .48,.44,.55; wardrobe cabinet 1.55,.6,2.05; dresser cabinet 1.25,.48,.88; small_desk table 1.25,.62,.74; desk_chair chair .54,.52,.94; refrigerator appliance .73,.7,1.78; kitchen_oven appliance .68,.62,.9; kitchen_counter cabinet 1.26,.62,.92; kitchen_sink sink 1,.6,.95; wall_cabinet cabinet 1.06,.36,.76; pantry_shelf shelf 1.15,.48,1.8; dining_crockery dish .52,.32,.13; frying_pan pan .57,.28,.1; kettle pot .26,.24,.28; cutting_board board .43,.29,.045; toilet toilet .58,.69,.78; bathtub bath 1.75,.75,.58; bathroom_sink sink .62,.52,.83; medicine_cabinet cabinet .65,.22,.74; washing_machine appliance .64,.64,.86; clothes_dryer appliance .64,.64,.85; water_heater tank .61,.61,1.6; laundry_basket crate .57,.43,.49''',
 'survival': '''
workbench table 1.72,.76,.9; wooden_storage_crate crate .9,.62,.62; metal_storage_cabinet cabinet .84,.48,1.83; tool_chest crate .86,.44,.47; toolbox crate .48,.22,.22; hammer tool .15,.40,.08; crowbar tool .10,.70,.09; hatchet tool .2,.45,.11; shovel tool .21,1.12,.10; pickaxe tool .48,.87,.12; saw tool .13,.68,.09; flashlight flashlight .1,.31,.1; battery_lantern lantern .23,.23,.35; candle candle .17,.16,.19; camping_stove stove .38,.30,.24; wood_stove stove .77,.64,1.1; improvised_forge stove 1.08,.69,1.12; rainwater_collector collector 1,.94,1.58; water_barrel tank .65,.65,.92; jerry_can can .34,.19,.46; water_bottle bottle .1,.1,.27; backpack bag .4,.23,.54; basic_generator generator .78,.54,.63; fuel_container can .32,.21,.44; portable_battery crate .32,.19,.23; first_aid_box crate .38,.24,.22''',
 'construction': '''
wooden_wall_section wall 1,.2,2.55; wooden_floor_section panel 1,1,.15; wooden_foundation_support beam .24,.24,1.2; wooden_post beam .17,.17,2.48; wooden_beam beam 1,.18,.18; wooden_door door 1,.18,2.13; window_frame frame 1,.18,1.18; wooden_barricade barricade 1,.23,1.98; reinforced_wooden_barricade barricade 1,.25,2.03; wooden_stairs stairs 1.06,1.72,1.12; stone_wall_section wall 1,.28,2.4; stone_foundation panel 1,1,.27; brick_wall_section wall 1,.24,2.42; concrete_foundation panel 1,1,.30; concrete_wall_section wall 1,.27,2.5; metal_reinforced_wall wall 1,.27,2.44; metal_door door 1,.17,2.13; metal_support_beam beam .23,.23,2.46; steel_reinforcement_panel panel 1,.08,2.28; metal_fence_gate fence 1.13,.14,2; damaged_wooden_wall wall 1,.21,2.44; broken_brick_wall wall 1,.28,2.26; destroyed_barricade barricade 1,.26,1.35''',
 'combat': '''
revolver pistol .19,.08,.16; shotgun longgun .12,1,.23; hunting_rifle longgun .11,1.08,.24; compact_smg longgun .12,.60,.22; baseball_bat tool .08,.78,.08; ammunition_box crate .25,.16,.11; shotgun_shell_box crate .21,.13,.14; loose_ammo_pickup ammo .23,.16,.10; protective_vest vest .52,.25,.63; helmet helmet .28,.32,.25''',
 'consumables': '''
canned_food can .10,.1,.13; soup_can can .09,.09,.13; food_box crate .27,.16,.29; snack_package crate .15,.08,.21; large_water_container bottle .27,.25,.43; food_storage_crate crate .45,.33,.26; small_cooler crate .45,.32,.31; bandage_roll bandage .13,.13,.11; first_aid_kit crate .38,.14,.26; medicine_bottle bottle .11,.10,.20; tablet_packet crate .14,.06,.10; medical_bag bag .41,.22,.31; emergency_supply_box crate .56,.36,.38''',
 'vegetation': '''
healthy_pine pine 2.7,2.7,5.1; dead_pine pine 2.32,2.4,4.56; leafless_deciduous tree 3.3,3.1,4.7; small_leafy_tree tree 2.7,2.6,3.75; bush shrub 1.15,.98,.84; dead_shrub shrub 1.08,.91,.84; grass_clump grass .65,.48,.43; fallen_log log 2.55,.52,.48; tree_stump stump .72,.74,.52; rock rock .72,.55,.44; boulder rock 1.87,1.55,1.27''',
 'decorations': '''
trash_bin can .59,.51,.91; mailbox mailbox .33,.49,1.2; outdoor_bench bench 1.55,.62,.84; garden_table table 1.10,.68,.77; wooden_fence fence 1.90,.18,1.48; metal_fence fence 1.91,.16,1.62; streetlight streetlight .45,.35,4.35; road_sign sign .51,.21,2.4; traffic_cone cone .31,.31,.53; wooden_pallet panel 1.12,.8,.16; utility_pole pole .35,.35,4.45; abandoned_bicycle bike 1.62,.47,1.06''',
 'vehicles': '''
family_car vehicle 1.91,4.2,1.42; pickup_truck vehicle 2,5.02,1.73; police_car vehicle 1.99,4.67,1.49; delivery_van vehicle 2.1,5.15,2.51; utility_truck vehicle 2.31,5.6,2.35''',
 'map': '''
small_family_house mapbuilding 8,9,6.5; large_suburban_house mapbuilding 11,10,7.5; apartment_block mapbuilding 12,9,15; convenience_store mapbuilding 8,9,5; supermarket mapbuilding 17,13,6; diner mapbuilding 11,8,5.5; restaurant mapbuilding 9,10,6; fast_food mapbuilding 9,10,5; hardware_store mapbuilding 13,11,7.5; lumberyard mapbuilding 15,14,6; industrial_warehouse mapbuilding 18,14,10; scrapyard_building mapbuilding 13,10,7.5; gun_shop mapbuilding 8,9,5; shooting_range mapbuilding 16,11,6.5; police_station mapbuilding 16,12,9; clinic mapbuilding 11,11,6.5; pharmacy mapbuilding 8,9,5; veterinary_clinic mapbuilding 10,10,6.5; hospital mapbuilding 18,16,13; military_outpost mapbuilding 14,14,8; guard_tower tower 4,4,10; quarry_structure mapbuilding 15,12,7.5; gas_station mapbuilding 13,12,5; road_straight road 8,16,.4; road_curve road 12,12,.4; road_intersection road 12,12,.4; bridge bridge 8,19,2.2; railway_crossing road 12,12,.6; harbor_dock dock 10,16,1.5; pier dock 4,15,1.4; seawall wall 10,1.2,2; road_barrier barricade 4,.6,.9''',
 'characters': '''
survivor human .85,.36,1.78; ordinary_psycho human .85,.38,1.82; runner human .85,.37,1.78; brute human 1.12,.48,2.10; suicide_bomber human .94,.48,1.88'''
}
EXISTING={'GPT_dining_table','GPT_dining_chair','GPT_cooking_pot','GPT_handgun'}
LEGACY=[('dining_table','furniture','table',[1.4,.8,.75],.05),('dining_chair','furniture','chair',[.5,.55,.9],.05),('cooking_pot','survival','pot',[.36,.30,.26],.02),('handgun','survival','pistol',[.06,.23,.17],.01)]

def asset_manifest():
 items=[]
 for cat,block in MANIFEST.items():
  for part in block.split(';'):
   part=part.strip()
   if not part:continue
   name,kind,dimension=part.split()
   dim=[float(v) for v in dimension.split(',')]
   cell= .5 if cat=='map' else .2 if cat=='vegetation' else .1 if cat=='vehicles' else .1 if cat=='construction' else .01 if cat in ('combat','consumables') else .05
   items.append({'id':'GPT_'+name,'base_id':name,'name':name.replace('_',' ').title(),'category':cat,'kind':kind,'dimensions':dim,'voxel_size_m':cell})
 items.extend(dict(id='GPT_'+name,base_id=name,name=name.replace('_',' ').title(),category=cat,kind=kind,dimensions=dim,voxel_size_m=cell) for name,cat,kind,dim,cell in LEGACY)
 return items

class Voxel:
 def __init__(self,item):
  self.item=item
  self.size=[max(3,math.ceil(a/item['voxel_size_m'])) for a in item['dimensions']]
  if max(self.size)>256:raise ValueError('VOX grid too large '+item['id'])
  self.data={};self.nx,self.ny,self.nz=self.size;self.colors=dict(RGB)
 def set(self,x,y,z,color):
  x,y,z=int(x),int(y),int(z)
  if 0<=x<self.nx and 0<=y<self.ny and 0<=z<self.nz:
   self.data[(x,y,z)]=P[color]
 def R(self,v,idx):return max(0,min(self.size[idx],round(v*self.size[idx])))
 def box(self,x0,x1,y0,y1,z0,z1,c):
  p=[self.R(v,i) for i,t in enumerate([(x0,x1),(y0,y1),(z0,z1)]) for v in t] if False else None
  xa,xb=self.R(x0,0),self.R(x1,0);ya,yb=self.R(y0,1),self.R(y1,1);za,zb=self.R(z0,2),self.R(z1,2)
  for z in range(za,max(za+1,zb)):
   for y in range(ya,max(ya+1,yb)):
    for x in range(xa,max(xa+1,xb)):self.set(x,y,z,c)
 def disk(self,cx,cy,rx,ry,z0,z1,c,inside=0):
  za,zb=self.R(z0,2),self.R(z1,2)
  for z in range(za,max(za+1,zb)):
   for y in range(self.ny):
    for x in range(self.nx):
     d=(((x+.5)/self.nx-cx)/rx)**2+(((y+.5)/self.ny-cy)/ry)**2
     if inside*inside<=d<=1:self.set(x,y,z,c)
 def ball(self,cx,cy,cz,rx,ry,rz,c):
  xa=max(0,int((cx-rx)*self.nx));xb=min(self.nx,math.ceil((cx+rx)*self.nx))
  ya=max(0,int((cy-ry)*self.ny));yb=min(self.ny,math.ceil((cy+ry)*self.ny))
  za=max(0,int((cz-rz)*self.nz));zb=min(self.nz,math.ceil((cz+rz)*self.nz))
  for z in range(za,zb):
   for y in range(ya,yb):
    for x in range(xa,xb):
     d=(((x+.5)/self.nx-cx)/rx)**2+(((y+.5)/self.ny-cy)/ry)**2+(((z+.5)/self.nz-cz)/rz)**2
     if d<=1:self.set(x,y,z,c)
 def line(self,x0,y0,z0,x1,y1,z1,r,c):
  steps=int(math.hypot((x1-x0)*self.nx,(y1-y0)*self.ny,(z1-z0)*self.nz)*2)+2
  for s in range(steps+1):
   t=s/steps;self.ball(x0+(x1-x0)*t,y0+(y1-y0)*t,z0+(z1-z0)*t,r,r,r,c)

# Standalone parametric model families. Assets share a palette but geometry varies by type and name.
def generate(item):
 a=Voxel(item); b=a.box;d=a.disk;ball=a.ball;line=a.line
 n=item['base_id'];kind=item['kind'];metal=any(v in n for v in ['metal','steel','iron','ammo','police','medical']);white=any(v in n for v in ['medical','hospital','bath','sink','fridge','pharmacy'])
 wood='wood';frame='steel' if metal else 'darkwood'
 if kind=='table':
  for x in (.10,.82):
   for y in (.10,.79):b(x,x+.09,y,y+.11,0,.91,frame)
  b(.03,.97,.02,.98,.88,1,'lightwood');b(.12,.88,.09,.2,.73,.88,wood);b(.12,.88,.8,.92,.73,.88,wood)
  if n=='workbench':b(.14,.84,.17,.75,.25,.32,frame);b(.12,.25,.12,.3,.94,1,'steel')
 elif kind in ('chair','stool'):
  for x in (.11,.77):
   for y in (.12,.76):b(x,x+.11,y,y+.10,0,.57,wood)
  b(.03,.97,.08,.94,.53,.63,'lightwood');b(.15,.85,.15,.21,.29,.34,frame)
  if kind=='chair':
   for x in (.11,.77):b(x,x+.11,.12,.22,.54,1,wood)
   for z in (.70,.87):b(.16,.85,.13,.23,z,z+.08,'lightwood')
 elif kind=='sofa':
  b(.04,.96,.1,.95,.20,.43,frame);b(.07,.93,.15,.88,.4,.62,'slate');b(.07,.93,.06,.25,.45,1,'blue')
  for x in (.02,.83):b(x,x+.15,.08,.92,.4,.74,'charcoal')
  for x in (.1,.85):
   for y in (.12,.80):b(x,x+.06,y,y+.07,0,.20,wood)
  b(.18,.65,.3,.68,.61,.67,'cloth')
 elif kind=='bed':
  b(.02,.98,.05,.96,.06,.24,frame);b(.06,.94,.11,.92,.23,.42,'cloth');b(.07,.93,.35,.93,.39,.60,'blue');b(.04,.96,.07,.2,.09,1,wood)
  b(.14,.44,.18,.35,.43,.61,'plaster')
  if n=='double_bed':b(.55,.88,.18,.35,.43,.61,'plaster')
 elif kind=='cabinet':
  b(.04,.96,.05,.96,.02,1,'steel' if metal else wood);b(.10,.9,.02,.07,.15,.93,'lightwood' if not metal else 'steel')
  b(.46,.55,0,.05,.15,.92,frame)
  if n in ('dresser','nightstand','sideboard'):
   for z in (.2,.46,.70):b(.15,.86,0,.08,z,z+.12,'lightwood');b(.47,.53,0,.04,z+.03,z+.08,'steel')
  else:b(.38,.43,0,.045,.49,.65,'highlight');b(.58,.63,0,.045,.49,.65,'highlight')
  if n=='kitchen_counter':b(0,1,0,1,.88,1,'lightwood')
 elif kind=='shelf':
  for x in (.04,.89):b(x,x+.07,.05,.95,0,1,frame)
  for z in (.06,.30,.54,.78,.93):b(.07,.94,.05,.95,z,z+.07,'lightwood')
  for z in (.35,.57,.82):
   for x,c in ((.19,'brick'),(.43,'olive'),(.68,'blue')):b(x,x+.10,.16,.47,z,z+.11,c)
 elif kind=='screen':
  b(.02,.98,.1,.9,.1,.96,'charcoal');b(.08,.92,.04,.11,.15,.86,'black');b(.42,.58,.39,.65,0,.1,'steel')
 elif kind=='lamp':
  b(.30,.70,.31,.69,0,.05,'steel');b(.47,.54,.46,.54,.02,.79,'charcoal');b(.15,.85,.15,.85,.75,1,'cloth')
 elif kind=='rug':
  b(.02,.98,.02,.98,0,1,'brick');b(.11,.89,.11,.89,.72,1,'cloth');b(.17,.21,.11,.89,.93,1,'rust')
 elif kind=='appliance':
  b(.03,.97,.05,.95,0,1,'plaster' if white else 'steel');b(.08,.92,0,.07,.18,.76,'charcoal')
  if n=='refrigerator':b(.04,.96,0,.07,.49,.52,'steel');b(.78,.84,0,.08,.18,.38,'charcoal')
  else:
   d(.5,.5,.32,.33,.34,.73,'slate',.62);b(.16,.83,0,.06,.83,.89,'charcoal')
 elif kind=='sink':
  b(.03,.97,.06,.94,.53,.81,'steel');b(.13,.87,.17,.81,.70,.86,'charcoal');b(.34,.66,.69,.83,.75,1,'highlight');b(.12,.88,.13,.84,0,.56,'green')
 elif kind in ('dish','pan','pot','can','bottle','tank','bandage'):
  if kind=='dish':
   for x in (.30,.68):d(x,.51,.22,.34,0,1,'cloth',.65)
  elif kind=='pan':
   d(.38,.50,.36,.43,0,.55,'charcoal',.6);d(.38,.50,.29,.35,0,.09,'steel');b(.72,1,.43,.57,.12,.23,'darkwood')
  elif kind=='pot':
   d(.5,.5,.40,.40,0,.9,'steel',.7);d(.5,.5,.33,.33,0,.1,'charcoal');b(.03,.18,.35,.65,.48,.7,'charcoal');b(.82,.97,.35,.65,.48,.7,'charcoal')
   if n=='kettle':d(.5,.5,.38,.37,.86,.95,'steel');line(.28,.5,.82,.72,.5,.82,.06,'charcoal')
  elif kind=='bottle':
   d(.5,.5,.32,.31,0,.73,'slate' if 'water' in n else 'brick');d(.5,.5,.18,.20,.70,.90,'cloth');d(.5,.5,.22,.23,.88,1,'steel')
  elif kind=='bandage':
   d(.5,.5,.43,.44,.06,.95,'cloth',.25);d(.5,.5,.46,.46,.15,.22,'plaster')
  elif kind=='tank':
   d(.5,.5,.36,.37,.03,.95,'slate' if n=='water_barrel' else 'plaster');d(.5,.5,.39,.40,.82,.91,'steel',.85)
  else:
   d(.5,.5,.36,.37,0,.95,'green' if n=='trash_bin' else 'slate');d(.5,.5,.38,.40,.88,.96,'steel');b(.19,.81,.03,.13,.32,.62,'cloth')
 elif kind in ('crate','bag','generator','collector','stove','lantern','candle'):
  if kind=='crate':
   col='steel' if metal else 'wood';b(.05,.95,.05,.95,.02,.94,col);b(.03,.97,.03,.97,.88,1,'lightwood' if not metal else 'highlight')
   for x in (.13,.45,.79):b(x,x+.035,.02,.98,.08,.91,'charcoal' if metal else 'darkwood')
  elif kind=='bag':
   b(.18,.82,.15,.86,.05,.88,'olive' if n=='backpack' else 'cloth');b(.22,.78,.03,.18,.20,.55,'green');line(.25,.35,.84,.25,.63,.98,.05,'charcoal');line(.75,.35,.84,.75,.63,.98,.05,'charcoal')
  elif kind=='generator':
   b(.12,.87,.12,.88,.2,.86,'steel');b(.24,.75,.02,.15,.34,.72,'charcoal');b(.11,.9,.12,.2,.79,.9,'rust')
   for x in (.1,.87):
    for y in (.2,.79):ball(x,y,.17,.11,.12,.14,'black')
  elif kind=='collector':
   for x in (.1,.84):
    for y in (.1,.83):b(x,x+.07,y,y+.07,0,.95,'wood')
   d(.5,.5,.3,.31,.12,.79,'slate');d(.5,.5,.31,.32,.77,.83,'charcoal',.67);b(.08,.91,.09,.92,.87,.9,'olive')
  elif kind=='stove':
   b(.08,.92,.12,.91,.13,.84,'charcoal');b(.19,.82,.08,.14,.34,.72,'black');b(.28,.75,.06,.08,.39,.68,'rust');b(.4,.6,.48,.7,.83,1,'steel')
  elif kind=='lantern':
   d(.5,.5,.4,.39,0,.24,'charcoal');d(.5,.5,.33,.34,.19,.77,'cloth');d(.5,.5,.39,.40,.77,.87,'steel');line(.28,.5,.80,.72,.5,.80,.08,'charcoal')
  else:d(.5,.5,.39,.39,0,.18,'steel');d(.5,.5,.22,.22,.17,.92,'cloth');b(.45,.55,.45,.55,.89,1,'yellow')
 elif kind=='tool':
  b(.43,.57,.06,.92,.36,.58,'darkwood');
  if n in ('hammer','hatchet','pickaxe'):b(.16,.84,.78,.92,.35,.7,'steel')
  elif n=='shovel':b(.25,.75,.73,1,.17,.55,'steel')
  elif n=='saw':b(.2,.84,.23,.76,.2,.59,'highlight')
  elif n=='crowbar':b(.19,.59,.81,.98,.38,.58,'rust')
 elif kind in ('wall','panel','beam','door','frame','barricade','fence','stairs'):
  mat='steel' if metal else 'brick' if 'brick' in n else 'concrete' if any(x in n for x in ['stone','concrete','seawall']) else 'wood'
  if kind in ('wall','panel','beam'):
   b(.02,.98,.02,.98,0,1,mat)
   if kind=='wall':
    for z in (.17,.46,.76):b(0,1,.01,.08,z,z+.035,'darkwood' if mat=='wood' else 'charcoal')
    if n.startswith(('damaged','broken')):b(.42,.65,.01,.98,.36,.76,'black')
  elif kind=='door':
   b(.04,.96,.11,.9,0,1,mat)
   for z in (.19,.55):b(.15,.84,.07,.14,z,z+.24,'lightwood' if mat=='wood' else 'charcoal')
   b(.81,.86,.05,.09,.53,.58,'highlight')
  elif kind=='frame':
   b(.01,.13,.05,.95,0,1,mat);b(.86,.99,.05,.95,0,1,mat);b(.13,.87,.05,.95,.87,1,mat)
  elif kind=='barricade':
   for x in (.1,.83):b(x,x+.08,.25,.81,0,1,'darkwood')
   for z in (.10,.34,.62,.87):b(.02,.98,.13,.89,z,z+.13,'steel' if metal else 'wood')
  elif kind=='fence':
   for x in (.08,.46,.87):b(x,x+.05,.38,.62,0,1,mat)
   for z in (.23,.79):b(.02,.98,.38,.62,z,z+.07,mat)
   if metal:
    for i in range(2,9):b(i/10,i/10+.025,.39,.61,.24,.96,'charcoal')
  else:
   for i in range(6):b(.06,.94,i/6,(i+1)/6,0,(i+1)/6,'lightwood')
 elif kind in ('pistol','longgun','ammo','vest','helmet'):
  if kind=='pistol':
   b(.16,.84,.05,.95,.65,.91,'charcoal');b(.24,.75,.08,.52,.22,.66,'olive');b(.3,.7,.45,.77,.38,.46,'steel')
  elif kind=='longgun':
   b(.30,.72,.08,.97,.64,.79,'charcoal');b(.41,.62,.55,.98,.73,.84,'steel');b(.27,.73,.04,.39,.42,.64,'darkwood');b(.4,.61,.31,.52,.17,.45,'olive')
  elif kind=='ammo':
   for i in range(3):
    for j in range(2):b(.12+i*.25,.19+i*.25,.15+j*.38,.26+j*.38,.03,.76,'rust')
  elif kind=='vest':
   b(.19,.81,.17,.85,.09,.90,'olive');b(.3,.70,.04,.18,.14,.83,'charcoal');b(.42,.57,.02,.09,.4,.61,'steel')
  else:ball(.5,.5,.54,.43,.44,.43,'olive');b(.09,.91,.06,.26,.38,.58,'olive')
 elif kind in ('pine','tree','shrub','grass','log','stump','rock'):
  if kind=='pine':
   b(.44,.57,.43,.57,0,.82,'darkwood')
   for i in range(5):
    z=.22+i*.13;r=.30*(1-i*.13)
    line(.5,.5,z,.5-r,.36,z+.04,.045,'darkwood');line(.5,.5,z,.5+r,.64,z+.04,.045,'darkwood')
    if not n.startswith('dead'):
     ball(.5-r*.55,.44,z+.08,r*.82,r*.76,.08,'green');ball(.5+r*.55,.55,z+.08,r*.75,r*.7,.08,'leaf')
  elif kind=='tree':
   b(.43,.57,.43,.58,0,.71,'darkwood');line(.5,.5,.5,.19,.46,.86,.045,'wood');line(.5,.5,.49,.82,.6,.83,.045,'wood')
   if 'leafy' in n:ball(.5,.5,.81,.42,.4,.18,'leaf')
  elif kind=='shrub':
   ball(.5,.5,.45,.45,.45,.43,'darkwood' if 'dead' in n else 'olive')
   if 'dead' not in n:ball(.5,.55,.64,.35,.35,.26,'leaf')
  elif kind=='grass':
   for x in (.22,.41,.62,.8):
    for y in (.23,.54,.78):b(x,x+.1,y,y+.13,0,.83,'olive')
  elif kind=='log':b(.03,.97,.28,.72,.12,.75,'wood');b(.05,.95,.38,.62,.16,.70,'darkwood')
  elif kind=='stump':d(.5,.5,.41,.40,0,.91,'darkwood');d(.5,.5,.36,.35,.88,1,'lightwood')
  else:ball(.5,.5,.44,.47,.48,.44,'concrete');ball(.36,.37,.62,.27,.28,.30,'steel')
 elif kind in ('mailbox','bench','streetlight','pole','sign','cone','bike'):
  if kind=='mailbox':b(.45,.57,.44,.56,0,.79,'wood');b(.1,.9,.15,.85,.70,1,'slate');b(.82,.93,.3,.45,.75,.98,'brick')
  elif kind=='bench':
   for x in (.11,.82):
    for y in (.19,.78):b(x,x+.07,y,y+.08,0,.64,'charcoal')
   b(.04,.96,.17,.83,.51,.62,'lightwood');b(.03,.96,.06,.18,.68,.97,'wood')
  elif kind in ('streetlight','pole','sign'):
   b(.45,.57,.43,.57,0,1,'charcoal')
   if kind=='streetlight':b(.45,.93,.34,.66,.9,.96,'steel');b(.79,.99,.2,.8,.85,.93,'plaster')
   if kind=='sign':b(.12,.87,.11,.25,.69,.91,'slate')
   if kind=='pole':
    for z in (.35,.82):b(.1,.9,.44,.56,z,z+.05,'wood')
  elif kind=='cone':
   for i in range(a.nz):
    z=i/a.nz;d(.5,.5,.45*(1-z)+.08,.45*(1-z)+.08,z,(i+1)/a.nz,'white' if .36<z<.53 else 'rust')
   b(.02,.98,.02,.98,0,.07,'charcoal')
  else:
   for yy in (.21,.79):
    for x in range(a.nx):
     for z in range(a.nz):
      r=math.hypot((x+.5)/a.nx-.5,(z+.5)/a.nz-.33)
      if .25<r<.31:a.set(x,a.R(yy,1),z,'charcoal')
   line(.5,.2,.33,.5,.5,.63,.045,'rust');line(.5,.5,.63,.5,.8,.33,.045,'rust');line(.5,.2,.33,.5,.8,.33,.045,'steel')
 elif kind=='vehicle':
  color='slate' if 'police' in n else 'olive' if 'pickup' in n else 'plaster' if 'van' in n else 'brick'
  b(.06,.94,.08,.93,.13,.51,color)
  if n in ('delivery_van','utility_truck'):b(.12,.88,.35,.86,.49,.94,color)
  else:b(.14,.86,.27,.73,.49,.84,color)
  b(.18,.82,.29,.33,.55,.79,'glass');b(.18,.82,.68,.72,.55,.79,'glass')
  for x in (.07,.86):
   for y in (.2,.78):ball(x,y,.15,.10,.10,.17,'charcoal')
  if 'police' in n:b(.36,.64,.46,.55,.84,.96,'rust')
 elif kind in ('mapbuilding','tower','road','bridge','dock'):
  if kind=='mapbuilding':
   wall='plaster' if 'house' in n else 'olive' if 'military' in n else 'concrete' if any(w in n for w in ('hospital','warehouse','quarry')) else 'steel'
   roof='brick' if 'house' in n else 'slate' if 'police' in n else 'charcoal'
   b(.05,.95,.08,.93,0,.77,wall)
   if 'house' in n:
    for i in range(5):
     z=.74+i*.055;b(.02+i*.095,.98-i*.095,.06,.95,z,z+.06,roof)
   else:b(.03,.97,.05,.95,.74,.83,roof)
   if n in ('apartment_block','hospital'):b(.12,.88,.1,.88,.76,.97,wall)
   for x in (.17,.45,.73):
    b(x,x+.12,.01,.09,.31,.53,'glass')
    if n in ('apartment_block','hospital'):b(x,x+.12,.01,.09,.65,.79,'glass')
   b(.40,.60,0,.1,0,.34,'darkwood')
   if any(w in n for w in ('hospital','clinic','pharmacy','veterinary')):b(.46,.54,0,.06,.50,.7,'brick');b(.39,.61,0,.06,.56,.63,'brick')
   if n=='gas_station':b(.08,.92,.02,.3,.35,.43,'rust');b(.10,.16,.05,.22,0,.36,'steel');b(.81,.88,.05,.22,0,.36,'steel')
  elif kind=='tower':
   for x in (.12,.80):
    for y in (.12,.80):b(x,x+.07,y,y+.07,0,.84,'wood')
   b(.02,.98,.02,.98,.80,.91,'olive');b(0,1,0,1,.9,1,'charcoal')
  elif kind=='road':
   b(0,1,0,1,0,.85,'charcoal')
   if 'intersection' in n:b(.45,.56,0,1,.85,1,'yellow');b(0,1,.45,.56,.85,1,'yellow')
   elif 'curve' in n:b(.45,.55,.44,1,.85,1,'yellow');b(.45,1,.44,.55,.85,1,'yellow')
   else:
    for y in (.12,.45,.79):b(.45,.54,y,y+.12,.85,1,'yellow')
  elif kind=='bridge':
   b(.02,.98,0,1,.49,.67,'concrete')
   for x in (.04,.90):b(x,x+.06,0,1,.67,.96,'steel')
  else:
   b(.05,.95,0,1,.58,.82,'darkwood')
   for y in (.08,.27,.48,.68,.9):b(.02,.98,y,y+.06,.82,1,'wood')
 elif kind=='human':
  cloth='green' if n=='survivor' else 'brick' if n=='ordinary_psycho' else 'slate' if n=='runner' else 'charcoal' if n=='brute' else 'olive'
  b(.37,.64,.29,.69,.44,.78,cloth);b(.03,.39,.35,.65,.66,.76,cloth);b(.61,.97,.35,.65,.66,.76,cloth)
  for x in (.39,.53):b(x,x+.09,.35,.64,.12,.44,'darkwood')
  for x in (.37,.53):b(x,x+.11,.31,.71,0,.14,'charcoal')
  b(.40,.6,.40,.64,.78,.98,'skin');b(.40,.60,.40,.64,.95,1,'charcoal')
  if n=='suicide_bomber':b(.31,.70,.08,.29,.45,.69,'rust');b(.42,.57,.04,.09,.51,.61,'yellow')
  if n=='brute':b(.22,.78,.25,.76,.48,.57,'charcoal')
 else:b(.05,.95,.05,.95,0,.96,'wood')
 if len(a.data)<2 or len(a.data)>75000:raise ValueError((n,len(a.data)))
 return a

def chk(name,payload=b'',children=b''):
 return name.encode('ascii')+struct.pack('<II',len(payload),len(children))+payload+children

def vox_bytes(a):
 coords=sorted(a.data.items(),key=lambda p:(p[0][2],p[0][1],p[0][0]))
 xyz=b''.join(struct.pack('BBBB',x,y,z,c) for (x,y,z),c in coords)
 rgba=b''.join(bytes(RGB[i])+b'\xff' if i in RGB else b'\x00\x00\x00\xff' for i in range(1,257))
 children=chk('SIZE',struct.pack('<III',*a.size))+chk('XYZI',struct.pack('<I',len(coords))+xyz)+chk('RGBA',rgba)
 return b'VOX '+struct.pack('<I',150)+chk('MAIN',children=children)

def parse_vox(buf,item):
 a=Voxel(item)
 assert buf[:4]==b'VOX '
 off=20;rgba=None
 while off<len(buf):
  tag=buf[off:off+4];ln,sub=struct.unpack_from('<II',buf,off+4);start=off+12
  if tag==b'SIZE':
   a.size=list(struct.unpack_from('<III',buf,start));a.nx,a.ny,a.nz=a.size
  if tag==b'XYZI':
   count=struct.unpack_from('<I',buf,start)[0]
   for i in range(count):
    x,y,z,color=struct.unpack_from('BBBB',buf,start+4+i*4)
    a.set(x,y,z,next(iter(P)) if color==0 else list(P)[color-1] if False else 'wood')
    a.data[(x,y,z)]=color
  if tag==b'RGBA':
   rgba=[tuple(buf[start+4*i:start+4*i+3]) for i in range(256)]
  off=start+ln+sub
 if rgba:a.colors={i:rgba[i-1] for i in range(1,256)}
 return a

def validate_vox(a,buf):
 assert buf[:4]==b'VOX ' and struct.unpack_from('<I',buf,4)[0]==150
 assert buf[8:12]==b'MAIN'
 off=20;count=None;size=None
 while off<len(buf):
  tag=buf[off:off+4];ln,sub=struct.unpack_from('<II',buf,off+4);start=off+12
  if tag==b'SIZE':size=struct.unpack_from('<III',buf,start)
  if tag==b'XYZI':count=struct.unpack_from('<I',buf,start)[0]; assert len({tuple(buf[start+4+4*i:start+7+4*i]) for i in range(count)})==count
  off=start+ln+sub
 assert size==tuple(a.size) and count==len(a.data)

def iso_preview(a,angle='hero',dim=500):
 size=a.size
 camera={'hero':(.85,-1.15,1.25),'front':(.06,-1.0,.21),'side':(1.,.04,.21)}[angle]
 def unit(vec):
  s=math.sqrt(sum(x*x for x in vec));return tuple(x/s for x in vec)
 eye=unit(camera);right=unit((-eye[1],eye[0],0));up=unit((-eye[0]*eye[2],-eye[1]*eye[2],eye[0]**2+eye[1]**2))
 def dot(a,b):return sum(x*y for x,y in zip(a,b))
 corners=[(x,y,z) for x in (0,size[0]) for y in (0,size[1]) for z in (0,size[2])]
 p=[(dot(x,right),dot(x,up)) for x in corners]
 mx=(min(x for x,y in p)+max(x for x,y in p))/2;my=(min(y for x,y in p)+max(y for x,y in p))/2
 dx=max(x for x,y in p)-min(x for x,y in p);dy=max(y for x,y in p)-min(y for x,y in p)
 scale=min((dim-95)/max(dx,1),(dim-120)/max(dy,1))
 def project(v):return(dim/2+(dot(v,right)-mx)*scale,dim/2+15-(dot(v,up)-my)*scale)
 img=Image.new('RGB',(dim,dim),(20,33,40));draw=ImageDraw.Draw(img)
 draw.ellipse((dim*.12,dim*.82,dim*.88,dim*.91),fill=(12,21,26))
 sides=[((1,0,0),[(1,0,0),(1,1,0),(1,1,1),(1,0,1)]),((-1,0,0),[(0,0,1),(0,1,1),(0,1,0),(0,0,0)]),((0,1,0),[(0,1,0),(1,1,0),(1,1,1),(0,1,1)]),((0,-1,0),[(1,0,0),(0,0,0),(0,0,1),(1,0,1)]),((0,0,1),[(0,0,1),(1,0,1),(1,1,1),(0,1,1)]),((0,0,-1),[(1,1,0),(1,0,0),(0,0,0),(0,1,0)])]
 faces=[];occupied=a.data
 for (x,y,z),color in occupied.items():
  for normal,offset in sides:
   if dot(normal,eye)<=0:continue
   nx,ny,nz=[u+v for u,v in zip((x,y,z),normal)]
   if (nx,ny,nz) in occupied:continue
   pts=[project((x+ox,y+oy,z+oz)) for ox,oy,oz in offset]
   light=.70+max(0,dot(normal,unit((-.7,-.15,1))))*.25
   rgb=tuple(min(255,round(v*light)) for v in a.colors[color]);faces.append((dot((x+.5,y+.5,z+.5),eye),pts,rgb))
 faces.sort(key=lambda f:f[0])
 for _,pts,rgb in faces:draw.polygon(pts,fill=rgb)
 draw.rounded_rectangle((12,10,dim-12,54),8,fill=(33,49,56))
 font=ImageFont.load_default()
 draw.text((21,18),a.item['id'].replace('GPT_','').replace('_',' ').title()[:38],fill=(240,223,194),font=font)
 draw.text((22,38),f"GPT · {a.item['category']} · {angle}",fill=(158,178,181),font=font)
 draw.text((16,dim-20),f"{len(a.data)} voxels · {a.item['voxel_size_m']} m cell",fill=(166,181,187),font=font)
 return img

def output(root:Path,only_missing=True):
 assets=asset_manifest(); output_catalog=[];count=0;counts=defaultdict(int)
 for item in assets:
  ident=item['id'];cat=item['category'];folder=root/'models'/cat/ident; preview=root/'previews'/cat/ident
  folder.mkdir(parents=True,exist_ok=True);preview.mkdir(parents=True,exist_ok=True)
  source=folder/f'{ident}.vox'
  if not (only_missing and source.exists()):
   a=generate(item);data=vox_bytes(a);validate_vox(a,data);source.write_bytes(data)
   meta=dict(schema_version=1,id=ident,base_id=item['base_id'],creator='GPT',name=item['name'],category=cat,revision=1,status='candidate',source=source.name,
    voxel_size_m=item['voxel_size_m'],source_axes={'right':'+X','front':'+Y','up':'+Z'},godot_forward='-Z',pivot_voxel=[a.nx/2,a.ny/2,0],dimensions_m=[round(x*item['voxel_size_m'],3) for x in a.size],occupied_voxels=len(a.data),material_roles=list(P),game_integration=[],notes='Independent procedural first-pass GPT model; native MagicaVoxel application verification pending')
   (folder/'model.json').write_text(json.dumps(meta,indent=2)+'\n')
   count+=1
  if not source.exists():continue
  a=parse_vox(source.read_bytes(),item)
  for angle in ('hero','front','side'):
   image=preview/f'{angle}.png'
   if not image.exists():iso_preview(a,angle).save(image,optimize=True)
  counts[cat]+=1
  output_catalog.append(dict(id=ident,base_id=item['base_id'],creator='GPT',name=item['name'],category=cat,status='candidate',revision=1,source_path=source.relative_to(root).as_posix(),metadata_path=(folder/'model.json').relative_to(root).as_posix(),preview_path=(preview/'hero.png').relative_to(root).as_posix(),game_integrations=[]))
 return output_catalog,count,dict(counts)

def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.')
 root.mkdir(parents=True,exist_ok=True)
 models,n,counts=output(root)
 # Preserve other creator's catalog records and legacy four GPT models if present.
 cat=root/'catalog.json'
 old=json.loads(cat.read_text()) if cat.exists() else {'schema_version':1,'library':'SirenVoxelLibrary','description':'Curated editable voxel assets','models':[]}
 current={m['id']:m for m in old.get('models',[])}
 for m in models:current[m['id']]=m
 old['models']=list(current.values())
 cat.write_text(json.dumps(old,indent=2)+'\n')
 manifest={'schema_version':1,'creator':'GPT','scope':'Complete first-pass catalog','items':asset_manifest(),'existing_gpt_models':['GPT_dining_table','GPT_dining_chair','GPT_cooking_pot','GPT_handgun']}
 docs=root/'docs';docs.mkdir(exist_ok=True);(docs/'GPT_catalog_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
 # Self-contained local thumbnail catalog works when opened from a clone.
 gallery=root/'gpt_gallery';gallery.mkdir(exist_ok=True)
 styles='body{font:14px system-ui;background:#101a20;color:#e8e6dc;margin:0}header{padding:20px 4vw;background:#20343d;position:sticky;top:0}header h1{margin:0}main{padding:16px 4vw}section h2{padding-top:15px}.grid{display:grid;grid-template-columns:repeat(auto-fill,minmax(180px,1fr));gap:12px}.card{background:#1c2c34;border:1px solid #3b5259;border-radius:7px;overflow:hidden}.card img{width:100%;display:block}.card a{color:#e8cda0}.card p{padding:8px;margin:0;font-size:12px}nav a{color:#dfc79e;margin-right:12px}'
 cats=sorted({r['category'] for r in old['models'] if r['id'].startswith('GPT_')})
 html=['<!doctype html><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>GPT Sirens Catalog</title>',f'<style>{styles}</style>',f'<header><h1>GPT · Sirens Asset Foundry</h1><p>{len([r for r in old["models"] if r["id"].startswith("GPT_")])} candidates. Review models individually before approval.</p><nav>'+''.join(f'<a href="#{c}">{c}</a>' for c in cats)+'</nav></header><main>']
 for c in cats:
  html.append(f'<section id="{c}"><h2>{c}</h2><div class="grid">')
  for r in old['models']:
   if r['category']!=c or not r['id'].startswith('GPT_'):continue
   img='../'+r['preview_path'];vox='../'+r['source_path'];html.append(f'<article class="card"><img loading="lazy" src="{img}"><p><a href="{vox}">{r["id"]}</a></p></article>')
  html.append('</div></section>')
 (gallery/'index.html').write_text(''.join(html)+'</main>')
 print(json.dumps({'new_models_this_run':n,'GPT_models_in_catalog':sum(m['id'].startswith('GPT_') for m in old['models']),'categories':counts,'folder':str(root)},indent=2))
if __name__=='__main__':main()