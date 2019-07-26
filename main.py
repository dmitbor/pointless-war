import sys
import pygame
import threading
import time
# import math
import random
from units.soldier import Soldier
from units.squad import Squad
from units.target import Target
from battlefield.objective import Objective
from misc.name_handle import Name_Handler
from misc.var_calcs import two_point_distance
from misc.faction import Faction
from misc.cam_data import Camera_Data
from misc.data_store import Data_Store


def DrawTargetLine(Screen, Unit, Cam_Ref):
    zl = cam_data.get_zoom_mod()
    cam_off = Cam_Ref.ret_cam_offset()
    cam_pad = Cam_Ref.get_zoom_padding()
    cam_mod = [cam_off[0] + cam_pad[0], cam_off[1] + cam_pad[1]]
    if Unit.get_move_target() is not None:
        pygame.draw.line(Screen, (50, 50, 50), ((Unit.get_x() + cam_mod[0]) / zl, (Unit.get_y() + cam_mod[1]) / zl), ((Unit.get_move_target().get_x() + cam_mod[0]) / zl, (Unit.get_move_target().get_y() + cam_mod[1]) / zl), 2)
    # pygame.display.flip()


def DrawFaceLine(Screen, Unit, Cam_Ref):
    zl = cam_data.get_zoom_mod()
    cam_off = Cam_Ref.ret_cam_offset()
    cam_pad = Cam_Ref.get_zoom_padding()
    cam_mod = [cam_off[0] + cam_pad[0], cam_off[1] + cam_pad[1]]
    pygame.draw.line(Screen, (100, 50, 100), ((Unit.get_x() + cam_mod[0]) / zl, (Unit.get_y() + cam_mod[1]) / zl), ((Unit.calculate_next_loc()[0] + cam_mod[0]) / zl, (Unit.calculate_next_loc()[1] + cam_mod[1]) / zl), 2)
    # pygame.display.flip()


def DrawUnit(Screen, Unit, Cam_Ref):
    zl = Cam_Ref.get_zoom_mod()
    cam_off = Cam_Ref.ret_cam_offset()
    cam_pad = Cam_Ref.get_zoom_padding()
    cam_mod = [cam_off[0] + cam_pad[0], cam_off[1] + cam_pad[1]]
    if type(Unit) == Soldier:
        ufc = Unit.my_squad.squad_faction.get_fac_color()
        color = (ufc[0], ufc[1], ufc[2])
        pygame.draw.rect(Screen, color, ((Unit.get_x() - 5 + cam_mod[0]) / zl, (Unit.get_y() - 5 + cam_mod[1]) / zl, 10 / zl, 10 / zl))
    elif type(Unit) == Objective:
        Unit.draw(Screen, zl, cam_mod)
    else:
        color = (30, 30, 30)
        pygame.draw.rect(Screen, color, ((Unit.get_x() - 5 + cam_mod[0]) / zl, (Unit.get_y() - 5 + cam_mod[1]) / zl, 10 / zl, 10 / zl))
    # pygame.display.flip()


def add_obj(obj_list):
    rand_x = 0
    rand_y = 0
    while True:
        pre_valid = True
        rand_x = random.randint(20, 540)
        rand_y = random.randint(20, 450)
        for exst_obj in obj_list:
            distance = two_point_distance(rand_x, rand_y, exst_obj.get_x(), exst_obj.get_y())
            if distance < 100.0:
                pre_valid = False
        if pre_valid is True:
            break
    obj = Objective()
    obj.set_location(rand_x, rand_y)
    obj_list.append(obj)


def add_squad(soldier_list, squad_list, faction, obj_list):
    new_squad = Squad()
    set_x = random.randint(20, 590)
    set_y = random.randint(20, 460)
    sldrs_in_sqd = []
    for x in range(0, 5):
        soldat = Soldier(name_handler, new_squad)
        soldat.set_location(set_x + random.randint(-10, 10), set_y + random.randint(-10, 10))
        soldier_list.append(soldat)
        sldrs_in_sqd.append(soldat)
    new_squad.assign_to_squad(sldrs_in_sqd)
    new_squad.set_first_as_lead()
    new_squad.set_faction(faction)
    new_squad.give_ref_obj(obj_list)
    new_squad.find_objective()
    squad_list.append(new_squad)
    new_squad = None


def add_test_factions(faction_list):
    faction_list.append(Faction("First", [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
    faction_list.append(Faction("Second", [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
    faction_list.append(Faction("Third", [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))
    faction_list.append(Faction("Fourth", [random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)]))


def add_more_squads(data_handler):
    for obj in data_handler.ret_objs():
        if obj.get_owner() is not None:
            add_squad(data_handler.ret_solds(), data_handler.ret_squads(), obj.get_owner(), data_handler.ret_objs())


def game_logic(data_handler):
    while True:
        # Go through each Squad
        for squad in data_handler.ret_squads():
            squad.get_cur_mission().check_completion(squad)
            squad.clear_completed_mission()
            squad_soldiers = squad.squad_members
            # For every soldier:
            # Move Soldier. Draw Soldier and Facing. Draw Target Lines.
            for soldat in squad_soldiers:
                if soldat.is_alive():
                    soldat.next_action(data_handler)
        data_handler.set_rspw_tmr(data_handler.ret_rspw_tmr() + 1)
        if data_handler.ret_rspw_tmr() == 100:
            add_more_squads(data_handler)
            data_handler.set_rspw_tmr(0)
        time.sleep(0.1)


pygame.init()
pygame.key.set_repeat(500, 100)
window_size = [640, 480]

print("Wah")

cam_data = Camera_Data(window_size)
name_handler = Name_Handler()
data_handler = Data_Store()

trgt = Target()
trgt.set_location(200, 250)

add_test_factions(data_handler.ret_facts())

for x in range(0, len(data_handler.ret_facts()) * 2):
    add_obj(data_handler.ret_objs())

# Add 3 Squads per Faction
for index, x in enumerate(range(1, len(data_handler.ret_facts()) * 3 + 1)):
    add_squad(data_handler.ret_solds(), data_handler.ret_squads(), data_handler.ret_facts()[index % len(data_handler.ret_facts())], data_handler.ret_objs())

# for sqd in data_handler.ret_squads():
#     sqd.find_objective()

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption('Pointless War')

gl_thread = threading.Thread(target=game_logic, args=(data_handler,), daemon=True)
gl_thread.start()

while True:
    for event in pygame.event.get():
        # print(event.type)
        if event.type == 12:
            sys.exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            m_pos = pygame.mouse.get_pos()
            trgt.set_location(m_pos[0], m_pos[1])
        if event.type == pygame.KEYDOWN:
            # print("Down")
            # print(event.key)
            shift_press = False
            if pygame.key.get_mods() == 1 or pygame.key.get_mods() == 2:
                shift_press = True

            # Zoom In
            if event.key == 45:
                cam_data.add_zoom()
            # Zoom Out
            elif event.key == 61:
                cam_data.red_zoom()
            # Up
            elif event.key == 273:
                cam_data.go_direction("up", shift_press)
            # Right
            elif event.key == 275:
                cam_data.go_direction("right", shift_press)
            # Down
            elif event.key == 274:
                cam_data.go_direction("down", shift_press)
            # Left
            elif event.key == 276:
                cam_data.go_direction("left", shift_press)

    # Clear Screen
    screen.fill((0, 0, 0))

    # Draw Objectives
    for obj in data_handler.ret_objs():
        DrawUnit(screen, obj, cam_data)

    for soldat in data_handler.ret_solds():
        if soldat.is_alive():
            DrawUnit(screen, soldat, cam_data)
            DrawFaceLine(screen, soldat, cam_data)
            DrawTargetLine(screen, soldat, cam_data)
    DrawUnit(screen, trgt, cam_data)
    aaa = pygame.font.Font('freesansbold.ttf', 15).render(str(data_handler.ret_rspw_tmr() / 10), True, (255, 255, 255))
    screen.blit(aaa, aaa.get_rect())

    pygame.display.flip()
    time.sleep(0.1)
