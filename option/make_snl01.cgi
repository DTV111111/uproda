#!/usr/bin/perl
#============================================#
# �e�g�ёΉ��p�̉摜�쐬 (R7 NEW)
#============================================#
# 2014.11.23 �ŐV��imagemagick�œ����悤�ɏC���i�V�W�I�V�e�B�[�Y�v���X�Ή��j
# i10L��im.cgi�̃T���l�C��1�Ԃ������̂ŁA�G���[�ɂȂ��Ă���B�Ώ��K�v�B
# 2013.02.05 PNG�̑傫�ȃt�@�C�����ɁA�T���l�C���傪�ł��Ȃ������o�O���C��
# 2011.06.07 �����������̂��߁A�Ҏ󂯉摜�쐬�@�\��p�~
# 2010.10.12 �A�j��/CG��p�̏k�����W�b�N��ǉ�
# 2010.10.12 �c�����DIET�𔻒f���郍�W�b�N��p�~����(���p�I�łȂ�����)
# 2010.10.08 �f�W�J������f���ɔ����A�t�@�C���̐�����1900����11000�Ɋg��
# 2010.10.08 �p�^�[���}�b�`�̏C��
# 2010.10.08 ���[�v�J�E���^�[�I�[�o�̃o�O���C��
# 2008.06.03 WVGA�t������ɍ��킹�Ďd�l�ύX
# 2005.09.24 �傫�ȃI���W�i���t�@�C���̏ꍇ�A�����Ń_�C�G�b�g�ł���悤�ɂ���
# 2005.09.18 SO505��p�R�[�h�폜
# 2005.09.18 L-mode�V�F�A����ɂ���p�t�@�C���쐬�𒆎~����
# 2002.09.04 update
#
# �e�g�тŌ�����悤�ɏk���摜�����
#
sub make_snl_file{

	local($convert_option);		# �ϊ��I�v�V����
	local($snl_future_bit);		# �g�їp���̏����g���r�b�g
	local($snl_ext);		# �g�їp�̎��ۂ̊g���q

	local($ttmp_file_size);		# �t�@�C���̃T�C�Y�i�o�C�g�j
	undef @SNL_FILE_STAT;		# �t�@�C��������ێ�����z��

	local($ishot_iL_size);		# ishot-L�t�@�C���̃T�C�Y�i�o�C�g�j
	local($ttmp_hw_type)="yokonaga";# �ʐ^�̏c���A�������
	local($ttmp_tenchi_mode)="12";	# �ʐ^�̓V�n
	local($ttmp_conv_log)="<BR>�ϊ����O�J�n<BR>";	# �ϊ����O

	local($ttmp_white_paper_flag)=0;	# eBook(����)�t���O
	local($ttmp_white_paper_xy)=640;	# eBook(����)�𑜓x

	# �I���W�i���摜���_�C�G�b�g�������̂ɒu��������
	if($diet_org_img eq ""){
	  $diet_org_img=1;
	}

	# Diet��̏c�������T�C�Y
	if($MICRO_DIET{'VHLIMIT'} eq ""){
	  $MICRO_DIET{'VHLIMIT'}="1024x768";
	}

	if($MICRO_DIET{'SIZE'} eq ""){
	  $MICRO_DIET{'SIZE'}="200"; # ���̃T�C�Y�ȏ�̂��̂��_�C�G�b�g��o�^����(�W��400KB)
	}
	
	# imgboard��im.cgi�̈Ⴂ���z��
	if($img_dir eq ""){
		$img_dir=$PM{'img_dir'}; # �p�X�̈Ⴂ���z��
	}
	local($tcontent_length)	=$ENV{'CONTENT_LENGTH'}; # imgboard��im.cgi�̈Ⴂ���z��
	$tcontent_length	=$web_get_file_size if($web_get_file_size>0);     

	# SNL�̈ꎞPPM�t�@�C����ۑ�����(1=�ۑ�����,0=�ۑ����Ȃ�)
	$store_snl_ppm_flag=0;

	# Web�p�[�c�̏ꍇ�̓T���l�C�������Ȃ� 2002.12
	if($FORM{'amode'} eq "post_webparts"){
		return;
	}

	# �摜�f�[�^�ȊO�̓T���l�C�������Ȃ� 2003.05
	if($new_fname!~ /\.(jpe?g|gif|png|bmp)$/i){
		return;
	}

	# ��CPU���זh�~(21MB) #2002.12 2010.10 2013.01update
	# ���̐ݒ�ł�200�`800MB���炢�̈ꎞ���������g���܂��B
	# �l�Ń�����2GB�ȏ��VPS�N���E�h�Ƃ����؂�ĂȂ�����A
	# ���~�b�^���Ίg�債�Ȃ��ł��������B
	if($tcontent_length > (21000*1024)){
#2002.12
#&error(" �e�ʃI�[�o CONTENT_LENGTH-$tcontent_length");
		return;
	}

	# ��CPU���זh�~(����Anime-GIF�΍�) #2003.05
	if(($tcontent_length > (300*1024))&&($new_fname =~ /gif/i)){
#		&error(" ���҃A�j���f�h�e�B���S���u�쓮 CONTENT_LENGTH-$tcontent_length");
		return;
	}

	# ���摜�̑f����m�� #2003.06
	if((-e "$img_dir/$new_fname")&&($imgsize_lib_flag== 1 )){	
		&imgsize("$img_dir/$new_fname");
		if(($IMGSIZE{'result'} ==1)&&($img_data_exists==1)){

			$ORGIMGSIZE{'type'}	="$IMGSIZE{'type'}";
			$ORGIMGSIZE{'width'}	="$IMGSIZE{'width'}";
			$ORGIMGSIZE{'height'}	="$IMGSIZE{'height'}";
			$ORGIMGSIZE{'hw_racio'}	="$IMGSIZE{'hw_racio'}";
			$ORGIMGSIZE{'square'}	= $IMGSIZE{'height'} * $IMGSIZE{'width'};

			$NOWIMGSIZE{'type'}	="$IMGSIZE{'type'}";
			$NOWIMGSIZE{'width'}	="$IMGSIZE{'width'}";
			$NOWIMGSIZE{'height'}	="$IMGSIZE{'height'}";
			$NOWIMGSIZE{'hw_racio'}	="$IMGSIZE{'hw_racio'}";
			$NOWIMGSIZE{'square'}	= $IMGSIZE{'height'} * $IMGSIZE{'width'};
		}
		undef %IMGSIZE;
	}

	# �c���A�����̔���
	if($ORGIMGSIZE{'hw_racio'} > 100){
		$ttmp_hw_type="tatenaga";
	}elsif($ORGIMGSIZE{'hw_racio'} == 100){
		$ttmp_hw_type="tatenaga";
	}else{
		$ttmp_hw_type="yokonaga";
	}
	

	# eBook(����)���o�t���O
	if(($tcontent_length > (300*1024))&&($new_fname =~ /\.png$/i)){
	 if(($ORGIMGSIZE{'width'} >= 2560)||($ORGIMGSIZE{'height'} >= 2560)){
		 if($tcontent_length < (800*1024)){
		 	$ttmp_white_paper_xy=2560;
		 	$ttmp_white_paper_flag=1;
		 }
	 }elsif(($ORGIMGSIZE{'width'} >= 2048)||($ORGIMGSIZE{'height'} >= 2048)){
		 if($tcontent_length < (700*1024)){
		 	$ttmp_white_paper_xy=2048;
		 	$ttmp_white_paper_flag=1;
		 }
	 }elsif(($ORGIMGSIZE{'width'} >= 1280)||($ORGIMGSIZE{'height'} >= 1280)){
		 if($tcontent_length < (400*1024)){
		 	$ttmp_white_paper_xy=1280;
		 	$ttmp_white_paper_flag=1;
		 }
	 }elsif(($ORGIMGSIZE{'width'} >= 1024)||($ORGIMGSIZE{'height'} >= 1024)){
		 if($tcontent_length < (300*1024)){
		 	$ttmp_white_paper_xy=1024;
		 	$ttmp_white_paper_flag=1;
		 }
	 }
	}

	
	if($ORGIMGSIZE{'hw_racio'} > 100){
		$ttmp_hw_type="tatenaga";
	}elsif($ORGIMGSIZE{'hw_racio'} == 100){
		$ttmp_hw_type="tatenaga";
	}else{
		$ttmp_hw_type="yokonaga";
	}
	
	# 30KB���T�C�Y���傫���ꍇ�́A�掿�d���̂��߂ɁA���T���v�����O���ԃt�@�C�������B
	# 30KB���T�C�Y���傫���ꍇ�́A�掿�d���̂��߂ɁAVGA���T�C�Y�t�@�C�������B
	if(($tcontent_length > (30*1024))&&($new_fname =~ /\.(jpe?g|png|bmp)$/i)){ # 2013.02 change

		# �g�їp�̃t�@�C���������i�����ɓ��ꂽ���̂������쐬�����j

# 2009.12 minaoshi
# jpg-pcvga,pc-wvga,,jpg-iL,jpg-iS, imgboard in use.



		@SNL_DATA=('jpg-pcvga','jpg-iL','jpg-iS','jpg-ps1');

		$new_snl_orig{'Low'}   = "snl"."$unq_id"."Low"."0"."\.ppm";	# �Ō��0�͏����g���p
		$new_snl_orig{'High'}  = "snl"."$unq_id"."High"."0"."\.ppm";	# �Ō��0�͏����g���p



		$ttmp_conv_log.=" ORG $tcontent_length Byte �n�C�T���v�����O���[�h���I������܂���<BR>";
	}else{
		# �g�їp�̃t�@�C���������i�����ɓ��ꂽ���̂������쐬�����j

		# 10�`30KB�̏ꍇ
		if($tcontent_length > (10*1024)){
		  @SNL_DATA=('jpg-iL','jpg-iS','jpg-ps1');
		# ishotS��g�т̏������摜�Ŋg�債�ĉ����Ȃ�̂�h��
		# check code TODO 2011.06
		
		}else{
		  @SNL_DATA=('jpg-iL','jpg-iS','jpg-ps1');
		}
		$new_snl_orig{'Low'}   = "snl"."$unq_id"."Low"."0"."\.ppm";	# �Ō��0�͏����g���p
		$ttmp_conv_log.=" $tcontent_length Byte ���[�T���v�����O���I������܂���<BR>";
	}


	# �g�їp�̍�����`�����L������
	undef @SNL_MADE_DATA;

	# �T���v�����O��f(�傫�������2��ŕ��ׂ��オ��̂Œ���)
	$SMPL_SIZE{'High'}="480x640";
	$SMPL_SIZE{'Low'} ="293x293";


# 2009.12 minaoshi
# jpg-iS,jpg-pcvga,jpg-iL,pc-wvga imgboard in use.

	# ���S�T�C�Y
	# �g�тŃ��������I�[�o���Ȃ��悤��
	# ��{�T�C�Y����⏬���ڂɒ�`����
	$SNL_SIZE{'jpg-ps1'}	="56x56"; # 2005.9 JPEG Packet Saver1

	# ����p�r
	# PC�T���l�C���ł��g�����(�V�n�t�]�s��)
	$SNL_SIZE{'jpg-pcvga'}	="480x480";	# VGA�T�C�Y # 2008.06 change

	# �����Ɍg�їp(�V�n�t�]�n�j)
# 2005.09 change NetFront�̎���ɍ��킹��
	$SNL_SIZE{'jpg-iL'}	="232x240";	# i-shot�C���^�[�l�b�g�T�C�Y(L)
	$SNL_SIZE{'jpg-iS'}	="120x120";	# i-shot�C���^�[�l�b�g�T�C�Y(S)


	# �����`�F�b�N
	unless(-e "$PM{'conv_prog'}"){
		&error(" �G���[�B�w�肳�ꂽ�ꏊ $PM{'conv_prog'} �ɉ摜�ϊ��\\�t\�g\������܂��� ");
		return;
	}
	unless($new_fname=~ /\.(jpe?g|gif|png|bmp)$/i){
		return;
	}

	$new_snl_fname   = "snl"."$unq_id";

	# �g�їp�����[���ʒm�p�Ɍg�їp�摜���쐬����

	if($ttmp_hw_type eq "yokonaga"){
		  $ty_option = " -rotate 90";
		  $ttmp_tenchi_mode= "3";
		  $ttmp_conv_log.=" 3����������<BR>";
		  $NOWIMGSIZE{'width'}	="$ORGIMGSIZE{'height'}";
		  $NOWIMGSIZE{'height'}	="$ORGIMGSIZE{'width'}";
		  $NOWIMGSIZE{'hw_racio'}=int(100*$ORGIMGSIZE{'width'}/$ORGIMGSIZE{'height'}) if($ORGIMGSIZE{'height'}>0);

# 2005.09 change
		  $ty_option = "";
		  $ttmp_tenchi_mode= "12";
		  $ttmp_conv_log.=" 12����������<BR>";
		  $NOWIMGSIZE{'width'}	="$ORGIMGSIZE{'width'}";
		  $NOWIMGSIZE{'height'}	="$ORGIMGSIZE{'height'}";
		  $NOWIMGSIZE{'hw_racio'}=int(100*$ORGIMGSIZE{'height'}/$ORGIMGSIZE{'width'}) if($ORGIMGSIZE{'width'}>0);

	# �c���摜�����o
	}else{
		$ty_option = "";
		# ���B��錾����Ă���ꍇ
		  $ttmp_tenchi_mode= "12";
		  $ttmp_conv_log.=" 12����������<BR>";
	}


	# �g�їp�����[���ʒm�p�Ɍg�їp�摜���쐬����

	# �ŏ��ɒ��ԃt�@�C�������(High Low�̂Q���)
	foreach(keys %new_snl_orig){
	 $ty_option="" if($_ eq "High"); # High�͉�]���Ȃ�

#2014.11 TMP �W�I�V�e�B�[�Y�V�T�[�o������蒲��
#$er_return = `$PM{'conv_prog'} \"$img_dir/$new_fname\"$ty_option -resize $SMPL_SIZE{$_} +profile \"\*\" $img_dir/$new_snl_orig{$_}`;
#&error(" $PM{'conv_prog'} \"$img_dir/$new_fname\"$ty_option -resize $SMPL_SIZE{$_} +profile \"\*\"  $img_dir/$new_snl_orig{$_} <BR>-��$er_return<BR>\n");

	 open  (COMMAND,"| $PM{'conv_prog'} -resize $SMPL_SIZE{$_} -strip \"$img_dir/$new_fname\"$ty_option $img_dir/$new_snl_orig{$_}") || &error(" �Ǘ��Ґݒ�ɃG���[������܂�<BR>�摜�ϊ��v���O����$PM{'conv_prog'}��������܂���B�摜�ϊ��v���O�����̃p�X���Ċm�F���Ă��������B<BR>\n");
	 close (COMMAND);


	 @SNL_FILE_STAT=stat("$img_dir/$new_snl_orig{$_}");	# �����𒲍�
	 $ttmp_file_size=$SNL_FILE_STAT[7];		# �t�@�C���T�C�Y���擾

	$ttmp_conv_log.="�T���v�����O conv���s $PM{'conv_prog'} -resize $SMPL_SIZE{$_} -strip \"$img_dir/$new_fname\"$ty_option $img_dir/$new_snl_orig{$_} <BR>$ttmp_file_size BYTE<BR>";


	 # R7�ō̗p����SNL�f�[�^�̃t�H�[�}�b�g�́A
	 # �g���q-�����g���p�ԍ�-�o�C�g/�g���q-�����g���p�ԍ�-�o�C�g/...�Ƃ���B
	 push(@SNL_MADE_DATA,"ppm-$_-$ttmp_file_size");

	}

	  foreach $snl_type(@SNL_DATA){


	    # GIF��i-mode�p256�F�p���b�g�Ńf�B�U�����O����

	    # ���FGIF�ɂ�����LZW�A���S���Y���͕K�{�ł͂Ȃ��B
	    # ImageMagick�ł̓f�t�H���g�ł�LZW=off�ł���̂ŁA
	    # ���̃X�N���v�g�ł́A���̖�������Ȃ����̂Ƃ���B
	    # �܂��A���̖��������X�C�b�`�@�\�����Ȃ��B
	    # �Ȃ��A���C�u�����ɂ����āALZW��configure���ĈӐ}�I��
	    # ON�ɂ���ꍇ�́Aconfigure�����l�� ���ȐӔC�ł��邱�Ƃ�
	    # �F�����Ă���A�g�����ƁB

	    if($snl_type =~ /gif/i){
		if(-e "i-palette.gif"){
		  $convert_option = "-map i-palette.gif";
		}
	    }
	    # JPEG��EXIF���̗]�v�ȃf�[�^�𗎂Ƃ��A�ł��邾���_�C�G�b�g����
	    if($snl_type =~ /jpe?g/){
		# 2014 update
		  $convert_option = " -strip";
	    }

	    # �V�n���[�h��12���ȊO�ɂȂ��Ă��āA����PC�p�̃T���l�C�������ꍇ�͉�]����
	    if(($snl_type =~ /pc/)&&($snl_type !~ /pcvga/)){
		if($ttmp_tenchi_mode == 9){
		  $convert_option .= " -rotate 90";
		}elsif($ttmp_tenchi_mode == 3){
		  $convert_option .= " -rotate -90";
		}
	    }

	    # iL�̓V���[�v�␳����
	    if($snl_type =~ /iL/){
#		  $convert_option .= " -sharpen 90";
	    }

	    # vga�n�͍��T���v���摜���g���B����ȊO�͒�T���v���摜���g��
	    if(($snl_type =~ /vga/i)&&($new_snl_orig{High} ne "")){
		  $convert_sample_type  = "High";
		  $convert_option 	= "";
	    }else{
		  $convert_sample_type = "Low";
	    }


	    # �g�їp�^�C�v���珫���g�����r�b�g�Ɗg���q�𕪗����Ďg��
	    ($snl_ext,$snl_future_bit)=split(/\-/,$snl_type);

	    $loop_count=0;
	    $tmp_size_ok=0;
	    # 2005.05.05 OK
	    $t_quality=75;

	    if($SNL_FSIZE{$snl_type}){
	     $ttmp_conv_log.="  $snl_type-�ϊ������J�n-��]�̃T�C�Y�̂��̂��ł���܂Ń��[�v�J�n<BR>";
	    }else{
	     $ttmp_conv_log.="  $snl_type-�ϊ������J�n(�ꔭ�^)<BR>";
	    }

	    # ��]�̃T�C�Y�̂��̂��ł���܂Ń��[�v����
	    while($tmp_size_ok!=1){

	      # 2005.09 �V�K
	      # �Ƃɂ���������������
	      if($snl_type =~ /ps1/){
			  $t_quality=25;# 
			  $convert_option .= " -quality $t_quality";
			  $mes_option .= "-$loop_count���- -quality $t_quality";
			  $ttmp_conv_log.="-$loop_count���-  -quality $t_quality<BR>";
	      }

	      $loop_count++;

		$ttmp_conv_log.=" conv���s ��size=$SMPL_SIZE{$convert_sample_type} -resize $SNL_SIZE{$snl_type} $convert_option$crop_option <BR>";

		$ttmp_conv_log.=" ���s $PM{'conv_prog'} -resize $SNL_SIZE{$snl_type}$convert_option$crop_option  \"$img_dir/$new_snl_orig{$convert_sample_type}\"  $img_dir/$new_snl_fname$snl_future_bit\.$snl_ext <BR>";

	      open  (COMMAND,"| $PM{'conv_prog'} -resize $SNL_SIZE{$snl_type}$convert_option$crop_option  \"$img_dir/$new_snl_orig{$convert_sample_type}\"  $img_dir/$new_snl_fname$snl_future_bit\.$snl_ext") || &error(" �Ǘ��Ґݒ�ɃG���[������܂�<BR>�摜�ϊ��v���O����$PM{'conv_prog'}��������܂���B�摜�ϊ��v���O�����̃p�X���Ċm�F���Ă��������B<BR>\n");
	      close (COMMAND);

	      @SNL_FILE_STAT=stat("$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext");
	      $ttmp_file_size=$SNL_FILE_STAT[7];	# �t�@�C���T�C�Y���擾

	      $ttmp_conv_log.=" �ϊ����� $snl_type -$loop_count- �T�C�Y $ttmp_file_size Byte<BR>";

	      # GIF�A�j���̎��ɃT���l�C���T�C�Y�����Ȃ��Ȃ�����C��
	      if(($ttmp_file_size eq "")&& ($ext=~ /gif/i) ){
		if( -e "$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext\.0"){
		   @SNL_FILE_STAT=stat("$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext\.0");
		   $ttmp_file_size=$SNL_FILE_STAT[7];	# �t�@�C���T�C�Y���擾
		}
	      }

	      if($SNL_FSIZE{$snl_type} eq ""){
		$tmp_size_ok=1;
	      }
	      if($ttmp_file_size <= $SNL_FSIZE{$snl_type}){ # 2005.09�C��
		$tmp_size_ok=1;
	      }
	      if($loop_count >= 4){ # ���S���u
		&error("loop_count $loop_count ���������܂��B$mes_option �ݒ���������Ă������� $snl_type-$ttmp_conv_log");
		$tmp_size_ok=1;
	      }

	      if(($tmp_size_ok==1)&&($SNL_FSIZE{$snl_type})){
		    $ttmp_conv_log.="  $snl_type-���[�v�I��<BR>";
	      }
	    }

	   # animation GIF���̕����^�Î~��ɑ΂���΍�
	   if($ext=~ /gif/i){
		if( -e "$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext\.0"){
			rename("$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext\.0","$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext");
			local($tmp_exit_flag)=0;
			local($tmp_add_ext)=1;
			while($tmp_exit_flag==0){
			  if(-e "$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext\.$tmp_add_ext"){
				unlink("$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext\.$tmp_add_ext");
				$tmp_add_ext++;
			  }else{
				$tmp_exit_flag=1;
			  }
			}
		}
	   
	   }



	   if(($snl_type =~ /gif/i)||($snl_type =~ /jpe?g/i)||($snl_type =~ /bmp/i)||($snl_type =~ /png/i)){
	    if((-e "$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext")&&($imgsize_lib_flag== 1 )){	
		&imgsize("$img_dir/$new_snl_fname$snl_future_bit\.$snl_ext");
		if(($IMGSIZE{'result'} ==1)&&($img_data_exists==1)){
		#	$IMGSIZE{'name'}�œn��;
		}else{
			undef %IMGSIZE;
		}
	    }
	   }

	    # �g�їp�t�@�C����������`�������X�g�ɋL��
	    push(@SNL_MADE_DATA, "$snl_ext-$snl_future_bit-$ttmp_file_size-$IMGSIZE{'width'}-$IMGSIZE{'height'}-$IMGSIZE{'hw_racio'}");

	    if($snl_type eq "jpg-iL"){
		$ishot_iL_size=$ttmp_file_size;
	    }
	    undef $convert_option; # clear
	  }

	# �I���W�i���̉摜���_�C�G�b�g����(30KB�ȉ��ɂ͐ݒ�ł��Ȃ��̂Œ��ӂ��邱��)
	# ���O�`�F�b�N
	if($diet_org_img == 1){

	  $ttmp_conv_log.="<BR> �I���W�i���̉摜���_�C�G�b�g���܂��B���ʎw�� $MICRO_DIET{'SIZE'} KB / ANIME_BBS_MODE $MICRO_DIET{'ANIME_BBS_MODE'}<BR>";
	
	  if($MICRO_DIET{'SIZE'} < 100){
		&error("�ݒ�G���[��MICRO_DIET{'SIZE'}��100KB�����ɐݒ�ł��܂���B�ݒ�l��ύX���Ă������� ");
	  }
	  
	  # ���ʂƃA�j���ōœK�l���Ⴄ�̂ŁA����𔻕ʂ��邽�߂̃t���O
	  $maybe_photo_flag=0;
	  
	  if(($tcontent_length > ($MICRO_DIET{'SIZE'}*1024))&&($new_fname =~ /\.(jpe?g|png|bmp)$/i)){ # 2013.02.05 change
		local($about_hw)=int($IMGSIZE{'hw_racio'}/10);
		if(($about_hw == 13)||($about_hw == 17)){
			$ttmp_conv_log.=" hw 13 or 17 ��maybe_photo_flag=1 <BR>";
			$maybe_photo_flag=1;
		}elsif(($about_hw == 7)||($about_hw == 5)){
			$ttmp_conv_log.=" hw 7 or 5 ��maybe_photo_flag=1 <BR>";
			$maybe_photo_flag=1;
		}else{
			$ttmp_conv_log.=" hw 13,17,7,5�ȊO�ł����B ��maybe_photo_flag=0 <BR>";
			$maybe_photo_flag=0;
		}
		$ttmp_conv_log.=" diet���܂� <BR>";
		$diet_org_img = 1;
	  }else{
		$ttmp_conv_log.=" diet���܂��� <BR>";
		$diet_org_img = 0;
	  }

	  # Debug�p
	  if($FORM{'name'} =~ /no_diet/i){
				$ttmp_conv_log.=" no_diet �w�肪�������̂ŁAdiet���܂��� <BR>";
				$diet_org_img = 0;
	  }
	}

	if($diet_org_img == 1){


	# �����f�W�J���ʐ^�Ő�M����ƁAXGA���T�C�Y�ł�500KB�ȏ�Ƒ傫���Ȃ�
	# �߂��錻�ۂɑΏ� #2010.10add

	# ���ʎʐ^�̏ꍇ
	if($maybe_photo_flag == 1){
	 if($tcontent_length > (1800*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }elsif($tcontent_length > (1400*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }elsif($tcontent_length > (550*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (400*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 85";
	 }elsif($tcontent_length > (300*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }elsif($tcontent_length > (250*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 75";
	 }elsif($tcontent_length > (200*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 70";
	 }elsif($tcontent_length > (150*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 60";
	 }elsif($tcontent_length > (100*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 50";
	 }else{
		$MICRO_DIET{'QUALITY'}="";
	 }

	# �A�j����p�f���̏ꍇ
	# �����掿
	}elsif($MICRO_DIET{'ANIME_BBS_MODE'} == 2 ){
	 if($tcontent_length > (1500*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
		$MICRO_DIET{'VHLIMIT'}="1920x1080";
	 }elsif($tcontent_length > (1000*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
		$MICRO_DIET{'VHLIMIT'}="1024x960";
	 }elsif($tcontent_length > (700*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
	 }elsif($tcontent_length > (550*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
	 }elsif($tcontent_length > (400*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
	 }elsif($tcontent_length > (300*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 96";
	 }elsif($tcontent_length > (250*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (200*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	# �A�j����200KB�ȉ��ł͋t�ɑ傫���Ȃ��Ă��܂����Ƃ�
	# ����̂ŁA200�ȉ��͐ݒ肳���Ȃ��ق����������낤�B
	 }elsif($tcontent_length > (150*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 85";
	 }elsif($tcontent_length > (100*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }else{
		$MICRO_DIET{'QUALITY'}="";
	 }
	# �A�j����p�f���̏ꍇ
	}elsif($MICRO_DIET{'ANIME_BBS_MODE'} == 1 ){
	 if($tcontent_length > (1500*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
		$MICRO_DIET{'VHLIMIT'}="1024x960";
	 }elsif($tcontent_length > (1000*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
		$MICRO_DIET{'VHLIMIT'}="1024x960";
	 }elsif($tcontent_length > (700*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
	 }elsif($tcontent_length > (550*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 95";
	 }elsif($tcontent_length > (400*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (300*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (250*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (200*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	# �A�j����200KB�ȉ��ł͋t�ɑ傫���Ȃ��Ă��܂����Ƃ�
	# ����̂ŁA200�ȉ��͐ݒ肳���Ȃ��ق����������낤�B
	 }elsif($tcontent_length > (150*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }elsif($tcontent_length > (100*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 75";
	 }else{
		$MICRO_DIET{'QUALITY'}="";
	 }	 
	# ���ʎʐ^�̏ꍇ
	}elsif($maybe_photo_flag == 1){
	 if($tcontent_length > (1800*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }elsif($tcontent_length > (1400*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }elsif($tcontent_length > (250*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 75";
	 }elsif($tcontent_length > (100*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 65";
	 }else{
		$MICRO_DIET{'QUALITY'}="";
	 }
	# �A�j����L���v�`���̏ꍇ
	}else{
	 if($tcontent_length > (1800*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (500*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 90";
	 }elsif($tcontent_length > (250*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 93";
	 }elsif($tcontent_length > (150*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 93";
	 }elsif($tcontent_length > (100*1024)){
		$MICRO_DIET{'QUALITY'}=" -quality 80";
	 }else{
		$MICRO_DIET{'QUALITY'}="";
	 }
	}

	$ttmp_conv_log.=" diet��Quality�� $MICRO_DIET{'QUALITY'}�Ɍ��肳��܂���  <BR>";


	# Debug�p
	if($FORM{'name'} =~ /resize_quality(\d+)/i){
	 if(($1 > 10)&&($1 < 101)){
		$ttmp_conv_log.=" resize_quality�w�肪�������̂�$MICRO_DIET{'QUALITY'}���� $1 �֏㏑�����܂�  <BR>";
		$MICRO_DIET{'QUALITY'}=" -quality $1";
	 }
	}

	$ttmp_new_fname="";
			
	# �X�}�z��^�u���b�g�̋���PNG(��ʃL���v�`��)�����o
	if(($tcontent_length > (350*1024))&&($new_fname =~ /\.(png|bmp)$/i)){

		$ttmp_conv_log.=" �X�}�z��^�u���b�g�̋���PNG(��ʃL���v�`��)�����o retina_flag  <BR>";

		$MICRO_DIET{'VHLIMIT'}="1280x1280";
	 	$MICRO_DIET{'QUALITY'}=" -quality 60";

		# ��{ ���摜�̉𑜓x�𑸏d����
		
		# �d�q�u�b�N�I�Ȃ��́i��f�̊��Ɍ��T�C�Y���������j��,�𑜓x��D�悳���邽�߂�retina�ۑ�����B
		# ���邢�͉B���@�\�Ƃ��Ė��O����retina�Ƃ��������������Ă���ƁA���̏ꍇ��retina�ۑ��Ƃ���

		if(($ORGIMGSIZE{'width'} >= 2560)||($ORGIMGSIZE{'height'} >= 2560)){
		 if(($FORM{'name'} =~ /retina/i)||($ttmp_white_paper_flag==1)){
			$MICRO_DIET{'VHLIMIT'}="2560x2560";
		 	$MICRO_DIET{'QUALITY'}=" -quality 45";
		 	$MICRO_DIET{'QUALITY'}=" -quality 35" if($ttmp_white_paper_flag==1); # eBook���o�t���O
		 }
		}elsif(($ORGIMGSIZE{'width'} >= 2048)||($ORGIMGSIZE{'height'} >= 2048)){
		 if(($FORM{'name'} =~ /retina/i)||($ttmp_white_paper_flag==1)){
			$MICRO_DIET{'VHLIMIT'}="2048x2048";
		 	$MICRO_DIET{'QUALITY'}=" -quality 45";
		 	$MICRO_DIET{'QUALITY'}=" -quality 35" if($ttmp_white_paper_flag==1); # eBook���o�t���O
		 }
	 	}elsif(($ORGIMGSIZE{'width'} >= 1280)||($ORGIMGSIZE{'height'} >= 1280)){
			$MICRO_DIET{'VHLIMIT'}="1280x1280";
		 	$MICRO_DIET{'QUALITY'}=" -quality 60";
	 	}elsif(($ORGIMGSIZE{'width'} >= 1156)||($ORGIMGSIZE{'height'} >= 1156)){
			$MICRO_DIET{'VHLIMIT'}="1156x1156";
		 	$MICRO_DIET{'QUALITY'}=" -quality 70";
	 	}elsif(($ORGIMGSIZE{'width'} >= 1024)||($ORGIMGSIZE{'height'} >= 1024)){
			$MICRO_DIET{'VHLIMIT'}="1024x1024";
		 	$MICRO_DIET{'QUALITY'}=" -quality 80";
	 	}elsif(($ORGIMGSIZE{'width'} >=  960)||($ORGIMGSIZE{'height'} >=  960)){
			$MICRO_DIET{'VHLIMIT'}="960x960";
		 	$MICRO_DIET{'QUALITY'}=" -quality 80";
	 	}elsif(($ORGIMGSIZE{'width'} >=  800)||($ORGIMGSIZE{'height'} >=  800)){
			$MICRO_DIET{'VHLIMIT'}="800x800";
		 	$MICRO_DIET{'QUALITY'}=" -quality 80";
	 	}elsif(($ORGIMGSIZE{'width'} >=  640)||($ORGIMGSIZE{'height'} >=  640)){
			$MICRO_DIET{'VHLIMIT'}="640x640";
		 	$MICRO_DIET{'QUALITY'}=" -quality 80";
	 	}else{
			$MICRO_DIET{'VHLIMIT'}="640x640";
		 	$MICRO_DIET{'QUALITY'}=" -quality 80";
	 	}

		$ttmp_new_fname="$new_fname";
		$ttmp_new_fname=~ s/\.png$/\.jpg/i;

		$ttmp_conv_log.=" �T�C�Y�k���̂��߁APNG��JPEG�ɒu�������܂��� �T�C�Y���� $MICRO_DIET{'VHLIMIT'} $MICRO_DIET{'QUALITY'} eBook����flag $ttmp_white_paper_flag xy_max $ttmp_white_paper_xy<BR>";

		$ttmp_conv_log.=" ���s$PM{'conv_prog'} -resize $MICRO_DIET{'VHLIMIT'}$MICRO_DIET{'QUALITY'} \"$img_dir/$new_fname\" $img_dir/$ttmp_new_fname <BR>";

	  open  (COMMAND,"| $PM{'conv_prog'} -resize $MICRO_DIET{'VHLIMIT'}$MICRO_DIET{'QUALITY'} \"$img_dir/$new_fname\" $img_dir/$ttmp_new_fname") || &error(" �Ǘ��Ґݒ�ɃG���[������܂�<BR>�摜�ϊ��v���O����$PM{'conv_prog'}��������܂���B�摜�ϊ��v���O�����̃p�X���Ċm�F���Ă��������B<BR>\n");
	  close (COMMAND);

		unlink("$img_dir/$new_fname");
		$new_fname="$ttmp_new_fname";

	}else{

	$ttmp_conv_log.=" ���s$PM{'conv_prog'} -resize $MICRO_DIET{'VHLIMIT'}$MICRO_DIET{'QUALITY'} -strip \"$img_dir/$new_fname\" $img_dir/$new_fname <BR>";
	
	# JPEG(�ʏ�͂������̏�����ʂ�)
	  open  (COMMAND,"| $PM{'conv_prog'} -resize $MICRO_DIET{'VHLIMIT'}$MICRO_DIET{'QUALITY'} -strip \"$img_dir/$new_fname\" $img_dir/$new_fname") || &error(" �Ǘ��Ґݒ�ɃG���[������܂�<BR>�摜�ϊ��v���O����$PM{'conv_prog'}��������܂���B�摜�ϊ��v���O�����̃p�X���Ċm�F���Ă��������B<BR>\n");
	  close (COMMAND);

	}


	  # ����̃T�C�Y��ύX
          @SNL_FILE_STAT=stat("$img_dir/$new_fname");
		$tcontent_length_diet=$SNL_FILE_STAT[7];	# �t�@�C���T�C�Y
		$ttmp_conv_log.=" $tcontent_length_diet ��diet����܂���  <BR>";

 	}

	  if($store_snl_ppm_flag != 1){
	   foreach(keys %new_snl_orig){
	    if(($new_snl_orig{$_} ne "")&&(-e "$img_dir/$new_snl_orig{$_}")){
	     unlink("$img_dir/$new_snl_orig{$_}");
	     # �������̂ŁA���X�g���甲��
	     shift(@SNL_MADE_DATA);
	    }
	   }
	  }

	$snl_location="$img_dir/$new_snl_fname";

	# SNL�Ƃ��đ��݂���f�[�^�̃��X�g�����
	foreach (@SNL_MADE_DATA){
		# �G���[���ɃS�~�������K�v�����邽�߁A�O���[�o���ϐ��ɂ���
		$existing_snl_type_list.="$_"."\/";
	}

	
undef %IMGSIZE; # �N���A

	# Debug�p
	if($FORM{'name'} =~ /snl_conv_log/i){
		&error(" �ϊ����O�m�F $ttmp_conv_log");
	}
}
#
1;

