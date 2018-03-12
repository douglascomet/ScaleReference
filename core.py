from maya import cmds

def create_dimension_grp(grp_name, len_value, width_value, height_value):
    '''Create Dimension Group for a reference of scale.

    Dimension Group is a set of 3 custom distance measurements to represent
    length, width, and height.

    Arguments:
        item {[type]} -- [description]
    '''

    dimens = ('length', 'width', 'height')

    for dimen in dimens:
        tuple_start_pos = ()
        tuple_end_pos = ()

        if dimen == 'length':
            tuple_start_pos = (len_value)/2.0, 0, 0
            tuple_end_pos = -(len_value)/2.0, 0, 0
        elif dimen == 'width':
            tuple_start_pos = 0, 0, (width_value)/2.0
            tuple_end_pos = 0, 0, -((width_value)/2.0)
        elif dimen == 'height':
            tuple_start_pos = 0, (height_value)/2.0, 0
            tuple_end_pos = 0, -((height_value)/2.0), 0

        # create Length Locators
        start_dimen_loc = cmds.spaceLocator(
            n=str(grp_name) + '_start' + dimen + '_loc_01',
            p=tuple_start_pos)

        end_dimen_loc = cmds.spaceLocator(
            n=str(grp_name) + '_end' + dimen + '_loc_01',
            p=tuple_end_pos)

        # Create length distanceDimension at generic 3d point
        # to be repurposed
        cmds.distanceDimension(startPoint=[1, 1, 1], endPoint=[-1, -1, -1])

        # Rename default distanceDimension locators' transform and
        # shape
        temp_loc_1 = cmds.rename('locator1', 'tempLoc_01')
        temp_rel_1 = cmds.listRelatives(temp_loc_1)
        loc_name_1 = cmds.rename(temp_rel_1, temp_loc_1 + 'Shape')

        temp_loc_2 = cmds.rename('locator2', 'tempLoc_02')
        temp_rel_2 = cmds.listRelatives(temp_loc_2)
        loc_name_2 = cmds.rename(temp_rel_2, temp_loc_2 + 'Shape')

        # Rename distanceDimension Node
        dist_dimen_new_name = cmds.rename(
            'distanceDimension1', str(grp_name) + '_dist' + dimen + '_01')
        temp_rel = cmds.listRelatives(dist_dimen_new_name)
        cmds.rename(temp_rel, dist_dimen_new_name + 'Shape')

        # Disconnect default distanceDimension locator and
        # distanceDimension Node
        cmds.disconnectAttr(
            str(loc_name_1) + '.worldPosition',
            str(dist_dimen_new_name) + 'Shape' + '.startPoint')
        cmds.disconnectAttr(
            str(loc_name_2) + '.worldPosition',
            str(dist_dimen_new_name) + 'Shape' + '.endPoint')

        # Connect new Locators to distanceDimension Node
        cmds.connectAttr(
            start_dimen_loc[0] + 'Shape.worldPosition',
            str(dist_dimen_new_name) + 'Shape' + '.startPoint')
        cmds.connectAttr(
            end_dimen_loc[0] + 'Shape.worldPosition',
            str(dist_dimen_new_name) + 'Shape' + '.endPoint')

        # Delete default Locators
        cmds.delete(temp_loc_1, temp_loc_2)

        if dimen == 'length':
            # group Lenth distanceDimension objects
            length_grp = cmds.group(
                start_dimen_loc, end_dimen_loc, dist_dimen_new_name,
                n=str(grp_name) + '_' + dimen + 'Dist_grp')

            set_color_overide(
                13, start_dimen_loc, end_dimen_loc, dist_dimen_new_name)

        elif dimen == 'width':
            width_grp = cmds.group(
                start_dimen_loc, end_dimen_loc, dist_dimen_new_name,
                n=str(grp_name) + '_' + dimen + 'Dist_grp')

            set_color_overide(
                6, start_dimen_loc, end_dimen_loc, dist_dimen_new_name)

        elif dimen == 'height':
            height_grp = cmds.group(
                start_dimen_loc, end_dimen_loc, dist_dimen_new_name,
                n=str(grp_name) + '_' + dimen + 'Dist_grp')

            set_color_overide(
                14, start_dimen_loc, end_dimen_loc, dist_dimen_new_name)

    cmds.group(
        length_grp, width_grp, height_grp,
        n=str(grp_name) + '_refDistance_grp')

def convert_units(up_or_down, cur_maya_unit, target_unit, len_value, width_value, height_value):
    if up_or_down:
        unit_convert_length = cmds.convertUnit(
            str(len_value), fromUnit=target_unit, toUnit=cur_maya_unit)
        unit_conv_width = cmds.convertUnit(
            str(width_value), fromUnit=target_unit, toUnit=cur_maya_unit)
        unit_conv_height = cmds.convertUnit(
            str(height_value), fromUnit=target_unit, toUnit=cur_maya_unit)

    else:
        unit_convert_length = cmds.convertUnit(
            str(len_value), fromUnit=cur_maya_unit, toUnit=target_unit)
        unit_conv_width = cmds.convertUnit(
            str(width_value), fromUnit=cur_maya_unit, toUnit=target_unit)
        unit_conv_height = cmds.convertUnit(
            str(height_value), fromUnit=cur_maya_unit, toUnit=target_unit)

    temp_str_length = unit_convert_length.split(target_unit)
    temp_str_width = unit_conv_width.split(target_unit)
    temp_str_height = unit_conv_height.split(target_unit)

    len_value = float(temp_str_length[0])
    width_value = float(temp_str_width[0])
    height_value = float(temp_str_height[0])

    return len_value, width_value, height_value

def get_up_axis():
    return cmds.upAxis(q=True, axis=True)

def get_scene_units():
    return cmds.currentUnit(query=True, linear=True)

def check_ref_grp_exists(grp_name):
    return cmds.objExists(str(grp_name) + '_refDistance_grp')

def delete_ref_grp(grp_name):
    cmds.delete(str(grp_name) + '_refDistance_grp')

def set_color_overide(index, *args):
    '''Sets overrideColor attribute.

    Arguments:
        index {int} -- Input index determines color of overrideColor
            attribute.
        *args {Maya objects} -- Inputs that would have their colors
            changed.
    '''

    for loc in args:
        if 'dist' in loc:
            cmds.setAttr(str(loc) + '.overrideEnabled', 1)
            cmds.setAttr(str(loc) + '.overrideColor', index)
        else:
            cmds.setAttr(loc[0] + '.overrideEnabled', 1)
            cmds.setAttr(loc[0] + '.overrideColor', index)
