/**
 * Created by paullichtenberger on 09.10.16.
 */


exports.validateReplik = function(req){
    req.checkBody('replik', 'Missing replik body').notEmpty().isStr();
    req.checkBody('scene_number', 'Missing or wrongly formated scene Number. Requires Int').notEmpty().isInt();
    req.checkBody('season_number', 'Missing or wrongly formated season Number. Requires Int').notEmpty().isInt();
    req.checkBody('episode_number', 'Missing or wrongly formated episode Number. Requires Int').notEmpty().isInt();
    req.checkBody('word_count', 'Missing or wrongly formated word_count Number. Requires Int').notEmpty().isInt();
    req.checkBody('replik_number', 'Missing or wrongly formated replik_number . Requires Int').notEmpty().isInt();
    req.checkBody('speaker', 'Missing or wrongly formated speaker. Requires String').notEmpty().isStr();
};