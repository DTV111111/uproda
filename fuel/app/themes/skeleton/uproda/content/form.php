<div class='section form'>
  <div class='container'>
    <?php echo \Form::open(['action' => 'image/upload', 'enctype' => 'multipart/form-data']); ?>
  	<?php echo \Form::csrf(); ?>
      <div class="row">
		<div class="four columns">
			<?php echo \Form::label($filelabel, 'upfile'); ?>
			<?php echo \Form::file('upfile', ['class' => 'u-full-width button-primary']); ?>
		</div>
		<div class="two columns"><?php echo \Form::label($dellabel, 'pass'); ?>
			<?php echo \Form::input('pass', null, ['class' => 'u-full-width', 'maxlength' => 8]); ?>
		</div>
		<div class="four columns"><?php echo \Form::label($commentlabel, 'comment'); ?>
			<?php echo \Form::input(['type' => 'text', 'name' => 'comment'], null, ['class' => 'u-full-width']); ?>
		</div>
      </div>
      <?php echo Form::submit('submit', $buttonlabel, ['class' => 'button-primary']);?>
    <?php echo Form::close(); ?>
  </div>
</div>
