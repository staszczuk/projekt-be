<?php
/* Smarty version 3.1.48, created on 2023-12-01 21:22:18
  from '/var/www/html/admin-dev/themes/new-theme/template/content.tpl' */

/* @var Smarty_Internal_Template $_smarty_tpl */
if ($_smarty_tpl->_decodeProperties($_smarty_tpl, array (
  'version' => '3.1.48',
  'unifunc' => 'content_656a407a9e3d56_95428486',
  'has_nocache_code' => false,
  'file_dependency' => 
  array (
    'e5706bf4d3c8244d18f4b9d6721d24822ae98891' => 
    array (
      0 => '/var/www/html/admin-dev/themes/new-theme/template/content.tpl',
      1 => 1701364022,
      2 => 'file',
    ),
  ),
  'includes' => 
  array (
  ),
),false)) {
function content_656a407a9e3d56_95428486 (Smarty_Internal_Template $_smarty_tpl) {
?>
<div id="ajax_confirmation" class="alert alert-success" style="display: none;"></div>


<?php if ((isset($_smarty_tpl->tpl_vars['content']->value))) {?>
  <?php echo $_smarty_tpl->tpl_vars['content']->value;?>

<?php }
}
}
