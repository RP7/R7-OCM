fid = fopen('../../../temp/rd.dat');
gd = fread(fid,192000*20,'int16');
fclose(fid);
giq = raw2iq(gd);
gd = resample(giq,6500,5760);

symbol_rate = (1625/6)*1e3; % GSM spec
num_frame = 64; % You'd better have at least 51 frames (one multiframe)
num_sym_per_slot = 625/4; % GSM spec
num_slot_per_frame = 8; % GSM spec

oversampling_ratio = 8;
decimation_ratio_for_FCCH_rough_position = 8;
decimation_ratio_from_oversampling = oversampling_ratio*decimation_ratio_for_FCCH_rough_position;

sampling_rate = symbol_rate*oversampling_ratio;

num_samples = oversampling_ratio * num_frame * num_slot_per_frame * num_sym_per_slot;
observe_time = num_samples/sampling_rate;
freq = 939.6e6;
sch_training_sequence = gsm_SCH_training_sequence_gen(oversampling_ratio);
normal_training_sequence = gsm_normal_training_sequence_gen(oversampling_ratio);

sampling_ppm = zeros(1,2);
carrier_ppm = zeros(1,2);

[FCCH_pos, FCCH_snr] = FCCH_coarse_position(gd(1:decimation_ratio_from_oversampling:end),8);
[FCCH_pos, r_correct, sampling_ppm(1), carrier_ppm(1)] = FCCH_fine_correction(gd, FCCH_pos, oversampling_ratio, freq);
[pos_info, r_correct, sampling_ppm(2)] = SCH_corr_rate_correction(r_correct, FCCH_pos, sch_training_sequence, oversampling_ratio);
[r_correct, carrier_ppm(2)] = carrier_correct_post_SCH(r_correct, pos_info, oversampling_ratio, freq);

SCH_demod(r_correct, pos_info, sch_training_sequence, oversampling_ratio);
