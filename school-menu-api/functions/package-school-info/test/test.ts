import { NeisCrawler } from "../src/data/NeisCrawler";
import { SchoolInfoDataAccessor } from "../src/data/SchoolInfoDataAccessor";
import { SchoolInfoService } from "../src/service/SchoolInfoService";
import { notStrictEqual } from "assert";
import admin from "firebase-admin";

admin.initializeApp({
    databaseURL: "localhost:8080",
    projectId: "dummy-firestore-id"
});

describe("[SCHOOL-INFO] School info parser", function() {

    this.timeout(100000);

    it('parses text from school info', function (done) {
        const neisCrawler = new NeisCrawler()
            .setParameters("서울");

        neisCrawler.get()
            .then(data => {
                notStrictEqual(data.length, 0);
            })
            .then(done);
    });
});

describe("[SCHOOL-INFO] School info service", function() {

    this.timeout(50000);

    it("saves keywords or datas", function (done) {
        const searchKeyword = "서울";

        const neisCrawler = new NeisCrawler().setParameters(searchKeyword);
        const schoolInfoDataAccessor = new SchoolInfoDataAccessor(admin.firestore());
        const schoolInfoService = new SchoolInfoService(neisCrawler, schoolInfoDataAccessor);

        schoolInfoService.getSchoolInfos(searchKeyword)
            .then(data => {
                notStrictEqual(data.length, 0);
            })
            .then(done);
    })
});
