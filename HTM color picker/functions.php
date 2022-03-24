<?php

global $avia_config;

add_theme_support('avia_template_builder_custom_css');

/*
 * if you run a child theme and dont want to load the default functions.php file
 * set the global var below in you childthemes function.php to true:
 *
 * example: global $avia_config; $avia_config['use_child_theme_functions_only'] = true;
 * The default functions.php file will then no longer be loaded. You need to make sure then
 * to include framework and functions that you want to use by yourself. 
 *
 * This is only recommended for advanced users
 */
// Modify the colors in the WP default editor (tiny mce) color picker widget
function htm_colors_in_mce_picker( $init ) {
$default_colours = '
"000000", "Black",
"993300", "Burnt orange",
"333300", "Dark olive",
"003300", "Dark green",
"003366", "Dark azure",
"000080", "Navy Blue",
"333399", "Indigo",
"333333", "Very dark gray",
"800000", "Maroon",
"FF6600", "Orange",
"808000", "Olive",
"008000", "Green",
"008080", "Teal",
"0000FF", "Blue",
"666699", "Grayish blue",
"808080", "Gray",
"FF0000", "Red",
"FF9900", "Amber",
"99CC00", "Yellow green",
"339966", "Sea green",
"33CCCC", "Turquoise",
"3366FF", "Royal blue",
"800080", "Purple",
"999999", "Medium gray",
"FF00FF", "Magenta",
"FFCC00", "Gold",
"FFFF00", "Yellow",
"00FF00", "Lime",
"00FFFF", "Aqua",
"00CCFF", "Sky blue",
"993366", "Brown",
"C0C0C0", "Silver",
"FF99CC", "Pink",
"FFCC99", "Peach",
"FFFF99", "Light yellow",
"CCFFCC", "Pale green",
"CCFFFF", "Pale cyan",
"99CCFF", "Light sky blue",
"CC99FF", "Plum",
"FFFFFF", "White"
';
$custom_colours = '
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"FFFFFF", "HTM Colors in next row",
"778f3b", "HTM Green",
"f1b717", "HTM Yellow",
"4f5c64", "HTM Dark Grey",
"e7e7e9", "HTM Light Grey",
"bf9e2d", "HTM YellowGreen",
"ec2028", "HTM Red",
"0ab7af", "HTM Turquoise",
"00a1e0", "HTM Blue",
"f15722", "HTM Orange",
"4e2f91", "HTM Purple"
';
$init['textcolor_map'] = '['.$default_colours.','.$custom_colours.']';
$init['textcolor_rows'] = 8; // expand colour grid to 8 rows
return $init;
}
add_filter('tiny_mce_before_init', 'htm_colors_in_mce_picker');
